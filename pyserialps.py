import sys
import drivers
import serial
import time
import psutil

COM_PORT_NAME 	= 	"COM3"
BAUD_RATE		=	9600
driver = drivers.Parallax27977Driver

def _run(portname, baudrate, driver_factory):
	with serial.Serial(portname, baudrate) as s:
		d = driver_factory(s)

		try:
			d.startup()

			while True:
				d.goto(0, 0)
				d.write("CPU {0:>6.1%} ".format(psutil.cpu_percent(interval=0.1) * 0.01))
				d.goto(0, 1)
				mem = psutil.virtual_memory()
				d.write("MEM {0:>6.1%} ".format(mem.percent * 0.01))
				time.sleep(0.65)

		except KeyboardInterrupt:
			d.shutdown()

def main(argv):
	_run(COM_PORT_NAME, BAUD_RATE, driver)

if __name__ == '__main__':
	main(sys.argv)
