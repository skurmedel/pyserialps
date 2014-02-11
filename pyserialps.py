import sys
import drivers
import serial

COM_PORT_NAME 	= 	"COM3"
BAUD_RATE		=	9600
driver = drivers.Parallax27977Driver

def _run(portname, baudrate, driver_factory):
	with serial.Serial(portname, baudrate) as s:
		d = driver_factory(s)

		try:
			d.startup()
			d.write("hello world o__o")
			d.goto(0, 1)
			d.write("hello terra")

			while True:
				pass

		except KeyboardInterrupt:
			d.shutdown()

def main(argv):
	_run(COM_PORT_NAME, BAUD_RATE, driver)

if __name__ == '__main__':
	main(sys.argv)
