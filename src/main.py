from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import Base, engine, get_db
from src.models.models import Domain, VisitsTime
from src.schemas.schemas import Urls

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_error_exception_handler(
        request: Request,
        exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"status": "bad request"},
    )


@app.post('/visited_links')
async def visited_links(urls: Urls, db: Session = Depends(get_db), ):
    visit_time = datetime.now()

    domains_from_request = set(x.host for x in urls.links)
    existing_domains_in_db = db.query(Domain) \
        .filter(Domain.domain_name.in_(domains_from_request))
    not_existing_domains = [
        x for x in domains_from_request.difference(
            set(_.domain_name for _ in existing_domains_in_db)
        )
    ]

    # for not existing before domains
    for x in not_existing_domains:
        domain = Domain(domain_name=str(x))
        domain_time = VisitsTime(domain=domain, visit_time=visit_time)
        db.add(domain, domain_time)

    # for existing before domains
    for x in existing_domains_in_db:
        domain_time = VisitsTime(domain=x, visit_time=visit_time)
        db.add(domain_time)

    db.commit()
    return {'status': 'ok'}


@app.get('/visited_domains')
async def get_visited_domains(
        time_from: Annotated[int, Query(alias='from')] = 0,
        time_to: Annotated[int, Query(alias='to')] = None,
        db: Session = Depends(get_db)
):
    time_from = datetime.utcfromtimestamp(time_from)
    time_to = datetime.now() if time_to is None \
        else datetime.utcfromtimestamp(time_to)

    if time_from > time_to:
        time_from, time_to = time_to, time_from

    visited_domains = (
        db.query(Domain.domain_name, VisitsTime.visit_time)
        .join(VisitsTime)
        .filter(VisitsTime.visit_time >= time_from,
                VisitsTime.visit_time <= time_to)
        .all()
    )
    return {
        'domains': {x.domain_name for x in visited_domains},
        'status': 'ok'
    }
