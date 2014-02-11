import drivers
import serial

COM_PORT_NAME 	= 	"COM3"
BAUD_RATE		=	9600
driver = drivers.Parallax27977Driver

def run():
	with serial.Serial(COM_PORT_NAME, BAUD_RATE) as s:
		d = driver(s)

		try:
			d.startup()
			d.write("hello")

			while True:
				pass

		except KeyboardInterrupt:
			d.shutdown()

def main():
	run()

if __name__ == '__main__':
	main()
