import drivers
import serial

COM_PORT_NAME 	= 	"COM3"
BAUD_RATE		=	9600
driver = drivers.Parallax27977Driver

def _run():
	with serial.Serial(COM_PORT_NAME, BAUD_RATE) as s:
		d = driver(s)

		try:
			d.startup()
			d.write("hello world o__o")

			while True:
				pass

		except KeyboardInterrupt:
			d.shutdown()

def main():
	_run()

if __name__ == '__main__':
	main()
