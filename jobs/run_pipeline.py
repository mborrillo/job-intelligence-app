from app.database import SessionLocal
from app import crud, matcher, scraper


def main():
    db = SessionLocal()
    run = crud.create_run(db, source="jooble")

    try:
        users = crud.get_users(db)
        if not users:
            print("No hay usuarios configurados. No se ejecuta el scraping.")
            crud.finish_run(db, run, status="no_users")
            return

        jobs = scraper.scrape_jooble()
        if not jobs:
            print("Scraper no devolvió ofertas. Revisa SCRAPER_BASE_URL.")
            crud.finish_run(db, run, status="no_jobs")
            return

        saved_jobs = 0
        for user in users:
            for job in jobs:
                if crud.job_exists(db, job["title"], job["url"], user.id, run.id):
                    continue
                score = matcher.calculate_score(job, user)
                crud.save_job(db, job, user.id, score, run.id)
                saved_jobs += 1

        crud.finish_run(db, run, status="success")
        print(f"Pipeline completado. Ofertas nuevas guardadas: {saved_jobs}")

    except Exception as e:
        crud.finish_run(db, run, status="failed")
        print(f"Error en el pipeline: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
