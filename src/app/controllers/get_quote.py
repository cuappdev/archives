from . import *
import random

class GetQuoteController(AppDevController):

  def get_path(self):
    return '/quote/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    quotes = [
        "You're only one workout away from a good mood.",
        "Life begins at the end of your comfort zone.",
        "Kick ass. Repeat.",
        "Yesterday you said tomorrow.",
        "Run the day. Don't let it run you.",
        "If no one thinks you can then you have to.",
        "Start unknown. Finish unforgettable.",
        "You can feel sore tomorrow or you can feel sorry tomorrow. You choose.",
        "Don't run away from challenges. Run over them. ",
        "Greatness is earned, never awarded.",
        "The harder you push, the more you are pulled.",
        "Giving up is simply not an option.",
        "Work hard and be proud of what you achieve.",
        "If it isn't trying, you're not trying hard enough.",
        "If it doesn't challenge you, it doesn't change you.",
        "Taking it easy won't take you anywhere."
    ]
    return random.choice(quotes)