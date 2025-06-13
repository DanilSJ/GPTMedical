from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    waiting_for_symptoms = State()
    waiting_for_analysis = State()
    waiting_for_question = State()
    waiting_for_medicine = State()
    waiting_for_female_consultation = State() 