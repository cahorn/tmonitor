import subprocess

def query():
    """
    Query the attached TEMPer device via temper-query command and parse the
    result.
    """
    p = subprocess.run(['/usr/local/bin/temper_query'], capture_output=True)
    p.check_returncode()
    temp = float(p.stdout.decode(encoding='ascii').strip())
    return temp

