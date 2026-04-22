# jobs/run_pipeline.py
from app.database import SessionLocal
from app import crud, matcher, scraper


def main():
    db = SessionLocal()
    try:
        users = crud.get_users(db)
        if not users:
            print("No hay usuarios configurados. No se ejecuta el scraping.")
            return

        jobs = scraper.scrape_jooble()
        if not jobs:
            print("Scraper no devolvió ofertas. Revisa la configuración de SCRAPER_BASE_URL.")
            return

        saved_jobs = 0
        for user in users:
            for job in jobs:
                if crud.job_exists(db, job["title"], job["url"], user.id):
                    continue
                score = matcher.calculate_score(job, user)
                crud.save_job(db, job, user.id, score)
                saved_jobs += 1

        print(f"Pipeline completado. Ofertas nuevas guardadas: {saved_jobs}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
