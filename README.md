## Steps to run the program locally: 
1. Set up a virtual environment and open the project directory
  - A recommended way of doing this as a beginner is through [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html).
3. Run `pip install -r requirements` in the terminal after you have entered the created Python virtual environment.
4. Then enter `flask db upgrade`.
5. Afterwards, run `flask run` and click on the link.

## Deploying it in [Render](https://render.com/)
1. Fork this [repository](https://github.com/FaisalTamanoJr/MS-InventorySystem) (render branch).
2. Sign in and create a PostgreSQL database.
  - Choose the best instance type for your needs.
4. Open the database in the site, click connect, and copy the internal database URL.
5. Go back to the dashboard and create a web service.
6. Fill the necessary details and select the forked repository as the repository for your web service (do not modify the default build command).
  - Choose the best instance type for your needs.
7. Enter this in the start command `flask db upgrade; gunicorn ms_inventory_system:app`.
8. Scroll down until you find the environment variables.
9. Type `DATABASE_URL` in one of the keys and enter the copied internal database url from step 3 to the value of the `DATABASE_URL`.
10. You can optionally set a `SECRET_KEY` variable for the program (recommended).
11. Create the web service and deploy it.
