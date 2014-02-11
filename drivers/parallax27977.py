import time

class Parallax27977InitError(Exception):
	def __init__(self):
		self.msg = "Drivers startup method not called."

class Parallax27977Driver:
	"""Supports Parallax Serial LCD #27977. Some features, like the Piezo speaker, are not implemented."""

	def __init__(self, serial_con):
		"""Inits a new driver, using serial_con as the serial interface."""
		self._started = False
		self._pos = (0, 0)
		self._s = serial_con

	@property
	def rows(self):
		return  2

	@property
	def columns(self):
		return 16

	def startup(self):
		"""Should be called before anything else is sent to the LCD. """
		# Display on, no cursor, no blink. Backlight on.
		self._s.write(bytes([0x16, 0x11]))
		self._started = True
		self.clear()

	def shutdown(self):
		"""Should be called as a shutdown procedure. """
		self._ensureStarted()

		self._s.write(bytes([0x15, 0x12]))
		self._started = False

	def goto(self, column, row):
		"""Move the cursor to (column, row), zero-indexed. Returns True on success, otherwise False."""
		self._ensureStarted()

		if row < 0 or column < 0:
			return False
		if row >= self.rows or column >= self.columns:
			return False

		pos = 0x80 + (row * 0x14) + column
		self._pos = (column, row)
		self._s.write(bytes([pos]))
		return True

	def clear(self):
		"""Clears the LCD from all text. Cursor position resets to (0, 0)."""
		self._ensureStarted()

		self._s.write(bytes([0x0C]))
		# Mandated by the documents, we must not send another command within 5 ms.
		time.sleep(0.010)
		self._pos = (0, 0)

	def write(self, text):
		"""Tries to write the text given. Throws on encoding errors.
		If the text is longer than what can be displayed, it will be truncated.

		ASCII characters < 32 will be stripped.
		"""
		self._ensureStarted()

		textlen = len(text)
		endpos = self._pos[0] + textlen
		if endpos > self.columns - 1:
			text = text[:self.columns - self._pos[0]]

		asciidata = text.encode("ASCII")
		# Remove tricky state altering characters.
		asciidata.strip(bytes(range(0, 31)))
		self._s.write(asciidata)
		self._pos = (self._pos[0] + len(asciidata), self._pos[1])

	def _ensureStarted(self):
		if not self._started:
			raise Parallax27977InitError()