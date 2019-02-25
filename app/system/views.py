# encoding:utf-8
import time
from flask import request, render_template
from flask_login import login_required

from .models import Stat
from .systeminfo import SystemInfo
from app.system import bp
from app import lm, db
from app.decorators import async 
  

# @async 
def run_system_info():
    i = 1
    while i < 2:
        time.sleep(2)
        systeminfo = SystemInfo()
        data = systeminfo.run_all_methods()
        # requests.post("http://127.0.0.1:5000/system", data=json.dumps(data))
        stat = Stat(host=data['host'], mem_free=data['mem_free'], mem_usage=data['mem_usage'],
                    mem_total=data['mem_total'], load_avg=data['load_avg'], time=data['time']
                    )
        db.session.add(stat)
        db.session.commit()
        i += 1


@bp.route('/system', methods=["GET", "POST"])
@login_required 
def system():
    if request.method == "POST":
        data = request.json
        stat = Stat(host=data.host, mem_free=data.mem_free, men_usage=data.men_usage, men_total=data.men_total, load_avg=data.load_avg, time=data.time)
        db.session.add(stat)
        db.session.commit()
        return "OK"
    else:
        stats = Stat.query.all()
        run_system_info()
        return render_template("system.html", title='system info')
