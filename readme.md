<h3 style="text-align: center;"> Documentasi </h3> 
<h1 style="text-align: center;">  CCTV PORTPASS </h1>


Stream CCTV aplikasi yang digunakan untuk play camera cctv secara realtime dengan memanfaatkan protocol RTSP pada camera cctv. Di kembangkan dengan pemrograman python 3.10 berbasis microweb (FLASK) image realtime stream.

1.	System Requirement 
    - Python 
    - Opencv
    - Flask
    - User & Password RTSP
    - Open Port 5000 (Server)
    - CCTV dan Server dalam satu jaringan

2. Setting & Configurasi Server
    - Port 5000 pada server wajib dibuka
    - Service Flask
    ```
    $: sudo touch /etc/systemd/system/flask.service
    ```

    ```
    [Unit]
    Description=Flask CCTV
    After=network.target
    StartLimitIntervalSec=0
    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    User=portpass
    ExecStart=/home/portpass/cctv_app/start.sh
    [Install]
    WantedBy=multi-user.target
    ```

3. Derectory App
    ````
    /home/portpass/cctv_app
        start.sh
        main.py
        templates/

    ````
    <strong> start.sh </strong>
    ````sh
    #!/bin/bash
    source /home/portpass/cctv_app/venv/bin/activate
    export FLASK_APP=/home/portpass/cctv_app/main.py
    flask run -h 0.0.0.0  --cert=cert.pem --key=priv_key.pem
    ````

4. Access URL <br>

    <strong> test stream </strong>
    ```
    https://10.14.41.209:5000/
    ```


    <strong> contoh access stream </strong>
    ```html
    <img async id="cctv_load" src= "https://10.14.41.209:5000/video_feed?user=admin&password=Admin123&ip=192.168.213.15" width="100%" />
    
    ```
    <strong>contoh thumbnail </strong>
    ```html
    <img async class="w-100 rounded-2"  id="gate_in" src= "https://10.14.41.209:5000/video_feed?user=admin&password=Admin123&ip=192.168.213.15"  >

5. Access via Online
    - access via online atau bisa diakses dari luar jaringan petro domain https://portpass.petrokimia-gresik.com port 5000 harus terbuka (bisa diakses tidak diblok sama firewall)