import speech_recognition as sr
import pyttsx3, time, chess

# global variables
r = sr.Recognizer() # CHANGE API KEY before deployment
board = chess.Board()

move_limit = 4 # HALF move limit MUST % 2 = 0
current_move = 0
game_complete = False
game_type = 1 # 0 = pvp, 1 = pvc, 2 = cvc (observer)

def speak_text(phrase):
	engine = pyttsx3.init()
	engine.say(phrase) 
	engine.runAndWait()

def give_error():
	print("Please try again")
	speak_text("sorry i did not get that")
	return False

def is_over():
	return current_move == move_limit - 1 or board.is_game_over()

def to_uci_notation(phrase):
	phrase = phrase.replace("knight", "N")
	phrase = phrase.replace("bishop", "B")
	phrase = phrase.replace("king", "K")
	phrase = phrase.replace("queen", "Q")
	phrase = phrase.replace("rook", "R")
	phrase = phrase.replace("to", "")
	phrase = phrase.replace(" ", "")
	
	return phrase

with sr.Microphone() as source:
	while not game_complete:
		should_increment = True
		print(board)

		r.adjust_for_ambient_noise(source)
		print("Move #" + str(current_move + 1) + " make your move:")

		try:
			audio = r.listen(source, timeout=3, phrase_time_limit=10)
		except sr.WaitTimeoutError:
			should_increment = give_error()
			continue

		try:
			input_text = r.recognize_google(audio)
			uci_input = to_uci_notation(input_text.lower())

			try:
				if chess.Move.from_uci(uci_input) in board.legal_moves:
					board.push(chess.Move.from_uci(uci_input))
					print("your move is: " + uci_input)
					speak_text(input_text.lower())
				else:
					print("illegal move: " + uci_input)
					speak_text("that is an illegal move")
					should_increment = False
					continue
			except ValueError:
				print("could not recognise move: " + uci_input)
				should_increment = give_error()
				continue
		except sr.UnknownValueError:
			should_increment = give_error()
			continue

		if is_over():
			print(board)
			break
		elif should_increment:
			current_move += 1
		else:
			continue
		