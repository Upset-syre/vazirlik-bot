import multiprocessing

workers = multiprocessing.cpu_count() + 1
# bind = 'unix:apiagro.sock'
bind = '0.0.0.0:5100'
# umask = 0o007
timeout = 0
#logging
accesslog = 'logs/access.log'
errorlog = 'logs/err.log'
capture_output = True
log_level = "debug"
loglevel = "debug"
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" '
# certificate = 'ssl/cer.crt'
# keyfile = 'ssl/cer.key'