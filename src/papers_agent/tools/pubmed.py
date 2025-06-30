from __future__ import annotations
import os, time
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel, Field, HttpUrl
from Bio import Entrez

Entrez.email = os.getenv("NCBI_EMAIL", "anonymous@example.com")
Entrez.api_key = os.getenv("NCBI_API_KEY")

class Paper(BaseModel):
    pmid: str = Field(..., description="PubMed ID")
    title: str
    abstract: str | None
    journal: str | None
    authors: List[str]
    pub_date: str
    mesh_terms: List[str] | None
    url: HttpUrl

def _esearch(q: str, mindate: str, maxdate: str, retmax=100,
             datetype: str = "edat") -> List[str]:
    with Entrez.esearch(db="pubmed", term=q,
                        mindate=mindate, maxdate=maxdate,
                        datetype=datetype, retmax=retmax) as h:
        return Entrez.read(h)["IdList"]

def _efetch(pmids: List[str]) -> List[Paper]:
    if not pmids:
        return []
    with Entrez.efetch(db="pubmed", id=",".join(pmids),
                       rettype="medline", retmode="xml") as h:
        recs = Entrez.read(h)

    out: list[Paper] = []
    for art in recs["PubmedArticle"]:
        med, art_d = art["MedlineCitation"], art["MedlineCitation"]["Article"]
        title = str(art_d.get("ArticleTitle", ""))
        abstract = (
            " ".join(str(t) for t in art_d["Abstract"]["AbstractText"])
            if "Abstract" in art_d else None
        )
        authors = [
            f"{a['LastName']} {a['Initials']}."
            for a in art_d.get("AuthorList", [])
            if "LastName" in a and "Initials" in a
        ]
        pub = art_d["Journal"]["JournalIssue"].get("PubDate", {})
        pub_date = f"{pub.get('Year','1900')}-{pub.get('Month','01')}-{pub.get('Day','01')}"
        mesh = [m["DescriptorName"] for m in med.get("MeshHeadingList", [])] or None

        out.append(Paper(
            pmid=str(med["PMID"]), title=title, abstract=abstract,
            journal=art_d["Journal"]["Title"], authors=authors,
            pub_date=pub_date, mesh_terms=mesh,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{med['PMID']}/",
        ))
    return out

def fetch_recent_papers(query: str,
                        days_back: int = 7,
                        retmax: int = 50,
                        delay: float = 0.34) -> List[Paper]:
    now = datetime.utcnow()
    mindate = (now - timedelta(days=days_back)).strftime("%Y/%m/%d")
    maxdate = now.strftime("%Y/%m/%d")
    ids = _esearch(query, mindate, maxdate, retmax)
    time.sleep(delay)
    return _efetch(ids)
