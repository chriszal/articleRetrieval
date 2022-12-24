### Clone project

```bash
git clone https://github.com/chriszal/articleRetrieval
cd articleRetrieval
```
### Start the application
--
while you are in the docker folder type

1. To start
   - docker-compose -p <project name> -f docker-compose.yml up --build -d
   
2. To stop and clean-up
   - docker compose -p  <project name> down 

### Endpoints
```bash
   /user/create --data '{"email":"example@gmail.com","city":"example","keywords":["war","health"]}'
```
```bash
   /user/edit/keywords
```
```bash
   /user/articles
```
```bash
   /user/delete
```
