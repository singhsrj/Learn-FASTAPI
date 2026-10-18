import uvicorn

if __name__=="__main__":
    #first argument, location of the app
    #second, host == domain . 0.0.0.0 - run on any available domain
    uvicorn.run("app.app_db:server",host="0.0.0.0",port=8000,reload=True)
