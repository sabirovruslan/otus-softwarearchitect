# otus-softwarearchitect

## HW-3 
Мониторинг приложения (Prometheus и Grafana)

### Запуск приложения
 - `sh start.sh`

### Скриншот Latency
![Alt Text](images/dashboard_latency.png)

### Скриншот RPS и Html statuses
![Alt Text](images/dashboard_rps.png)

### Скриншот Nginx Latency
![Alt Text](images/dashboard_nginx_latency.png)

### Скриншот Nginx RPS, http statuses и errors
![Alt Text](images/dashboard_nginx_rps.png)

### Скриншот CPU, Memory usage
![Alt Text](images/dashboard_cpu_and_memory.png)

### Скриншот Postgres
![Alt Text](images/dashboard_postgres.png)

### Скриншот Настройка алертинга
![Alt Text](images/alerting.png)

### Dashboards
 - [Latency and RPS (app metrics)](dashboards/dashboard.json)
 - [CPU and Memory usage](dashboards/dashboard_cpu_and_memory.json)
 - [Nginx ingress metrics](dashboards/dashboard_nginx.json)
 - [Postgres metrics](dashboards/dashboard_pg.json)