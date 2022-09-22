import random
import threading
from typing import Union

from ReyzuRobot.modules.helper_funcs.msg_types import Types
from ReyzuRobot.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from sqlalchemy.sql.sqltypes import BigInteger

DEFAULT_WELCOME_MESSAGES = [
    "{first} disini!",  # Discord welcome messages copied
    "Kamu siap {first}",
    "Teman-teman, {first} telah hadir.",
    "Hai {first}, muncullah.",
    "{first} datang seperti Singa.",
    "{first} telah bergabung dengan party kita.",
    "{first} baru bergabung. Beri saya motivasi?",
    "{first} baru saja bergabung dengan obrolan ngawur",
    "{first} baru bergabung. Semua anggota terlihat sibuk!",
    "Welcome, {first}. Tinggal sebentar dan dengarkan.",
    "Welcome, {first}. Kami mengharapkanmu ( ͡° ͜ʖ ͡°)",
    "Welcome, {first}. Kami harap Anda membawa pizza.",
    "Welcome, {first}. Tinggalkan sendalmu di dekat pintu.",
    "Swoooosh. {first} Baru saja mendarat.",
    "Kuatkan dirimu. {first} baru saja bergabung dengan obrolan.",
    "{first} baru bergabung. Sembunyikan pisang Anda.",
    "{first} baru saja tiba. Sepertinya OP - tolong nerf.",
    "{first} baru masuk ke chat.",
    "Eh {first} telah muncul di obrolan.",
    "Hai {first} munculah!",
    "Dimana {first}? Di grup ini?",
    "{first} nimbrunglah disini!",
    "{first} just baru saja muncul. Tolong non-aktifkan saya.",
    "Penantang mendekat! {first} telah muncul!",
    "Ini burung! Ini adalah pesawat! Tidak apa-apa, hanya saja {first}.",
    "Ini {first}! Memuji matahari! \o/",
    "Tidak akan pernah menyerah pada {first}. Tidak akan pernah mengecewakan {first}.",
    "Ha! {first} telah bergabung! Hai {firs}!",
    "Lihatlah kawan! {first} telah datang!",
    "Kami telah menunggumu {first}",
    "Berbahaya pergi sendiri, ambil {first}!",
    "{first} telah bergabung dengan obrolan! Ini sangat efektif!",
    "Salam sayang! {first} telah disini!",
    "{first} ada di sini, seperti yang dinubuatkan.",
    "{first} telah tiba. Yuk kita tinggal tidur.",
    "{first} Disini nimbrung ajah. Orangnya baik-baik",
    "Hai. Apakah itu {first} yang kucari selama ini?",
    "{first} telah bergabung. Ayo kita lanjut tidur!",
    "Mawar itu merah, violet itu biru, {first} I love you",
    "Welcome {first}, coba banned saya, ckckckck!",
    "Ini burung! Ini adalah pesawat! - Tidak, itu {first}!",
    "{first} lagi galau! - Ok.",  # Discord welcome messages end.
    "Assalamu'alaikum {first}!",
    "Hai, {first}. Jangan cuma nyimak, ayo ikut nimbrung",
    "{first} kamu sudah ketinggalan party",
    "Pendatang baru nih!",  # Tekken
    "Ok {firs} silahkan disimak!",
    "{first} baru saja masuk ke obrolan!",
    "Sesuatu baru saja jatuh dari langit! - Oh itu {first}.",
    "{first} Baru saja dideportasi ke sini!",
    "Hai, {first}, tunjukkan kartu pengenal anda",  # Hunter Hunter
    "Saya mencari jodoh, apakah itu {first}?.",  # One Punch man s2
    "Welcome {first}, Pergi bukanlah pilihan!",
    "Hai! ..Welcome {first}.",
    "{first} lakukan 100 push-up, 100 sit-up, 100 squat, dan lari 10km SETIAP HARI!!!",  # One Punch ma
    "Huh?\nSeorang perusuh baru saja bergabung?\oh bukan, dia hanyalah {first}.",  # One Punch ma
    "Hey, {first}, apa kamu lapar?",  # One Punch ma
    "Hey, {first}, berikan dompetmu!.",
    "Hey, {first}!, apa kamu kuat?",
    "Panggil owner! - {first} telah bergabung ke grup.",
    "{first} bergabung. kamu harus nyawer lagu buat kita semua.",
    "Lagi mager. {first} apa kamu mager?.",
    "Lagi malas nyapa orang, belom digaji aku bulan ini",
    "Kamu belum mandi?.",
    "Tempat ini harus memiliki WiFi gratis, karena saya merasakan koneksi.",
    "Bicaralah kawan, nimbrung saja",
    "Welcome {first}",
    "Welcome {first}, pacarmu tidak ada disini",
    "Hai {first}, selamat Datang di grup yang isinya orang gabut semua.",
    "Hola {first}, tetaplah waspada, terutama sama crocodile",
    "Hey {first}, beri kami sedikit kisah tentang anda",
    "Hai {first}\nIni bukan tempat yang aneh, grup ini orang-orangnya yang aneh.",
    "Oh, hey {first} apa pasdwor wi-fi mu?",
    "Hey {first}, Aku tahu apa yang akan kita lakukan hari ini",
    "{first} baru bergabung, waspada bisa jadi doi mata-mata.",
    "{first} bergabung dengan grup, dibaca oleh Mark Zuckerberg, CIA dan 35 lainnya.",
    "Welcome {first}, kamu tau monyet, diatas kita ini monyet.",
    "Hai semua mari kita sambut {first} yang baru bergabung.",
    "Hai {first}, Anda ingin tahu bagaimana saya mendapatkan bekas luka ini?",
    "Welcome {first}, lepas dulu maskermu, ayo kita vc",
    "Jaga diri {first}, Jaga jarak dengan para crocodile di grup ini",  # Corona memes lmao
    "Hai {first}, apa kamu suka nasi padang?",
    "Kamu disini sekarang {first}, keluarkan semua unek-unekmu",
    "{first} baru saja bergabung, sepertinya dia butuh teman curhat",
    "{first} baru bergabung, sepertinya perintah Pak Presiden",
    "Hai {first}, curhat aja jangan malu-malu?",
    "Yipee Kayaye {first} masuk grup.",
    "Welcome {first}, jika Anda seorang agen rahasia, tekan 1, jika tidak, mulailah percakapan",
    "{first}, Saya merasa kamu sendang lelah, ceritakan sedikit kisahmu disini",
    "Orang di grup ini mungkin pada sok asik, tapi sepertinya {first} beneran asik.",
    "Welcome {first}. Ngopilah dulu",
    "Welcome {first}, Istirahatlah dulu sejenak.",
    "Welcome {first}, semoga kamu bahagia selalu",
    "Semoga {first} orang yang kita cari selama ini.",
    "{first} baru bergabung. Hei, di mana owner, buatkan kopi dulu anggota baru?",
    "{first} telah bergabung.",
    "Tuan-tuan dan nyonya-nyonya, saya berikan kepada Anda ...  {first}.",
    "Lihatlah semua kelakuan anggota grup ini, {first} ayo nimbrung.",
    "Ah, {first} telah bergabung, tapi grupnya tetap sepi.",
    "{first} baru saja bergabung, tolong sapa saya mau istirahat dulu",  # One Piece Sanji
    "{first} baru bergabung, belikan dulu somay dia!",  # No Game No Life
    "{first} say Aschente to swear by the pledges.",  # No Game No Life
    "{first} telah bergabung, kampu bukan psikopat kan?!",  # Steins Gate
    "Inilah dia dukun cabul kita... {first}!",  # weeabo shit
    "Hai {first}, 1000-7 berapa?",  # tokyo ghoul
    "Hai...",  # hunter x hunter
    "Hai {first} salam kenal.",  # one Piece
    "Hey {first}...pernahkah kamu mendengar kata-kata indah?",  # BNHA
    "Tidak bisakah aku tidur sebentar di sekitar sini??",  # Kamina Falls – Gurren Lagann
    "Bangunlah kurangi rebahan {first}.",  # Hellsing
    "Kepasar beli mangga, ayo nimbrung aja..",  # Neon Genesis: Evangelion
    "Hai, welcome {first}",  # Pokemon
    "Hey {first}, Apakah Anda Menantang Saya?",  # Shaggy
    "Hah? Kamu belum mandi ya {first}?",  # jojo
    "Ho… mukatta kuruno ka?",  # jojo jap ver
    "Halo {first} mangga kalo mau cerita, cerita aja",  # jojo
    "Ho ho! {first} nyari apa kamu disini.",  # jojo
    "Hoho! Dewa juubun chikazukanai youi",  # jojo jap ver
    "Welcome, {first}. Jangan sungkan untuk cerita ya",  # jojo
    "Berapa banyak roti yang telah Anda makan dalam hidup Anda?",  # jojo
    "Kamu sudah makan belum {firs}!",  # jojo
    "Siapa lagi ini, halo {first} salam kenal.",  # jojo
    "Rerorerorerorerorero.",  # jojo
    "{first} baru saja masuk ke grup.",
    "I..it's..it's just {first}.",
    "Sugoi, Dekai. {first} Joined!",
    "{first}, apakah Anda tahu dewa kematian menyukai apel?",  # Death Note owo
    "Tunggu sebentar {first}. Saya akan mengambil keripik kentang .... dan memakannya",  # Death Note owo
    "Oshiete oshiete yo sono shikumi wo!",  # Tokyo Ghoul
    "Kaizoku ou ni...nvm wrong anime.",  # op
    "{first} just joined! Gear.....second!",  # Op
    "Omae wa mou....shindeiru",
    "Hey {first}, the leaf village lotus blooms twice!",  # Naruto stuff begins from here
    "{first} Joined! Omote renge!",
    "{first}! I, Madara! declare you the strongest",
    "{first}, this time I'll lend you my power. ",  # Kyuubi to naruto
    "{first}, welcome to the hidden leaf village!",  # Naruto thingies end here
    "In the jungle, you must wait...until the dice read five or eight.",  # Jumanji stuff
    "Dr.{first} Famed archeologist and international explorer,\nWelcome to Jumanji!\nJumanji's Fate is up to you now.",
    "{first}, this will not be an easy mission - monkeys slow the expedition.",  # End of Jumanji stuff
    "Remember, remember, the Fifth of November, the Gunpowder Treason and Plot. I know of no reason why the Gunpowder Treason should ever be forgot.",  # V for Vendetta
    "The only verdict is vengeance; a vendetta, held as a votive not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous.",  # V for Vendetta
    "Behind {first} there is more than just flesh. Beneath this user there is an idea... and ideas are bulletproof.",  # V for Vendetta
    "Love your rage, not your cage.",  # V for Vendetta
    "Get your stinking paws off me, you damned dirty ape!",  # Planet of the apes
    "Elementary, my dear {first}.",
    "I'm back - {first}.",
    "Bond. {first} Bond.",
    "Come with me if you want to live",
]
DEFAULT_GOODBYE_MESSAGES = [
    "{first} will be missed.",
    "{first} just went offline.",
    "{first} has left the lobby.",
    "{first} has left the clan.",
    "{first} has left the game.",
    "{first} has fled the area.",
    "{first} is out of the running.",
    "Nice knowing ya, {first}!",
    "It was a fun time {first}.",
    "We hope to see you again soon, {first}.",
    "I donut want to say goodbye, {first}.",
    "Goodbye {first}! Guess who's gonna miss you :')",
    "Goodbye {first}! It's gonna be lonely without ya.",
    "Please don't leave me alone in this place, {first}!",
    "Good luck finding better shit-posters than us, {first}!",
    "You know we're gonna miss you {first}. Right? Right? Right?",
    "Congratulations, {first}! You're officially free of this mess.",
    "{first}. You were an opponent worth fighting.",
    "You're leaving, {first}? Yare Yare Daze.",
    "Bring him the photo",
    "Go outside!",
    "Ask again later",
    "Think for yourself",
    "Question authority",
    "You are worshiping a sun god",
    "Don't leave the house today",
    "Give up!",
    "Marry and reproduce",
    "Stay asleep",
    "Wake up",
    "Look to la luna",
    "Steven lives",
    "Meet strangers without prejudice",
    "A hanged man will bring you no luck today",
    "What do you want to do today?",
    "You are dark inside",
    "Have you seen the exit?",
    "Get a baby pet it will cheer you up.",
    "Your princess is in another castle.",
    "You are playing it wrong give me the controller",
    "Trust good people",
    "Live to die.",
    "When life gives you lemons reroll!",
    "Well, that was worthless",
    "I fell asleep!",
    "May your troubles be many",
    "Your old life lies in ruin",
    "Always look on the bright side",
    "It is dangerous to go alone",
    "You will never be forgiven",
    "You have nobody to blame but yourself",
    "Only a sinner",
    "Use bombs wisely",
    "Nobody knows the troubles you have seen",
    "You look fat you should exercise more",
    "Follow the zebra",
    "Why so blue?",
    "The devil in disguise",
    "Go outside",
    "Always your head in the clouds",
]
# Line 111 to 152 are references from https://bindingofisaac.fandom.com/wiki/Fortune_Telling_Machine


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    should_welcome = Column(Boolean, default=True)
    should_goodbye = Column(Boolean, default=True)
    custom_content = Column(UnicodeText, default=None)

    custom_welcome = Column(
        UnicodeText,
        default=random.choice(DEFAULT_WELCOME_MESSAGES),
    )
    welcome_type = Column(Integer, default=Types.TEXT.value)

    custom_leave = Column(UnicodeText, default=random.choice(DEFAULT_GOODBYE_MESSAGES))
    leave_type = Column(Integer, default=Types.TEXT.value)

    clean_welcome = Column(BigInteger)

    def __init__(self, chat_id, should_welcome=True, should_goodbye=True):
        self.chat_id = chat_id
        self.should_welcome = should_welcome
        self.should_goodbye = should_goodbye

    def __repr__(self):
        return "<Chat {} should Welcome new users: {}>".format(
            self.chat_id,
            self.should_welcome,
        )


class WelcomeButtons(BASE):
    __tablename__ = "welcome_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line


class GoodbyeButtons(BASE):
    __tablename__ = "leave_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line


class WelcomeMute(BASE):
    __tablename__ = "welcome_mutes"
    chat_id = Column(String(14), primary_key=True)
    welcomemutes = Column(UnicodeText, default=False)

    def __init__(self, chat_id, welcomemutes):
        self.chat_id = str(chat_id)  # ensure string
        self.welcomemutes = welcomemutes


class WelcomeMuteUsers(BASE):
    __tablename__ = "human_checks"
    user_id = Column(BigInteger, primary_key=True)
    chat_id = Column(String(14), primary_key=True)
    human_check = Column(Boolean)

    def __init__(self, user_id, chat_id, human_check):
        self.user_id = user_id  # ensure string
        self.chat_id = str(chat_id)
        self.human_check = human_check


class CleanServiceSetting(BASE):
    __tablename__ = "clean_service"
    chat_id = Column(String(14), primary_key=True)
    clean_service = Column(Boolean, default=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<Chat used clean service ({})>".format(self.chat_id)


Welcome.__table__.create(checkfirst=True)
WelcomeButtons.__table__.create(checkfirst=True)
GoodbyeButtons.__table__.create(checkfirst=True)
WelcomeMute.__table__.create(checkfirst=True)
WelcomeMuteUsers.__table__.create(checkfirst=True)
CleanServiceSetting.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()
WELC_BTN_LOCK = threading.RLock()
LEAVE_BTN_LOCK = threading.RLock()
WM_LOCK = threading.RLock()
CS_LOCK = threading.RLock()


def welcome_mutes(chat_id):
    try:
        welcomemutes = SESSION.query(WelcomeMute).get(str(chat_id))
        if welcomemutes:
            return welcomemutes.welcomemutes
        return False
    finally:
        SESSION.close()


def set_welcome_mutes(chat_id, welcomemutes):
    with WM_LOCK:
        prev = SESSION.query(WelcomeMute).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        welcome_m = WelcomeMute(str(chat_id), welcomemutes)
        SESSION.add(welcome_m)
        SESSION.commit()


def set_human_checks(user_id, chat_id):
    with INSERTION_LOCK:
        human_check = SESSION.query(WelcomeMuteUsers).get((user_id, str(chat_id)))
        if not human_check:
            human_check = WelcomeMuteUsers(user_id, str(chat_id), True)

        else:
            human_check.human_check = True

        SESSION.add(human_check)
        SESSION.commit()

        return human_check


def get_human_checks(user_id, chat_id):
    try:
        human_check = SESSION.query(WelcomeMuteUsers).get((user_id, str(chat_id)))
        if not human_check:
            return None
        human_check = human_check.human_check
        return human_check
    finally:
        SESSION.close()


def get_welc_mutes_pref(chat_id):
    welcomemutes = SESSION.query(WelcomeMute).get(str(chat_id))
    SESSION.close()

    if welcomemutes:
        return welcomemutes.welcomemutes

    return False


def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return (
            welc.should_welcome,
            welc.custom_welcome,
            welc.custom_content,
            welc.welcome_type,
        )
    # Welcome by default.
    return True, random.choice(DEFAULT_WELCOME_MESSAGES), None, Types.TEXT


def get_gdbye_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.should_goodbye, welc.custom_leave, welc.leave_type
    # Welcome by default.
    return True, random.choice(DEFAULT_GOODBYE_MESSAGES), Types.TEXT


def set_clean_welcome(chat_id, clean_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id))

        curr.clean_welcome = int(clean_welcome)

        SESSION.add(curr)
        SESSION.commit()


def get_clean_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()

    if welc:
        return welc.clean_welcome

    return False


def set_welc_preference(chat_id, should_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_welcome=should_welcome)
        else:
            curr.should_welcome = should_welcome

        SESSION.add(curr)
        SESSION.commit()


def set_gdbye_preference(chat_id, should_goodbye):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_goodbye=should_goodbye)
        else:
            curr.should_goodbye = should_goodbye

        SESSION.add(curr)
        SESSION.commit()


def set_custom_welcome(
    chat_id,
    custom_content,
    custom_welcome,
    welcome_type,
    buttons=None,
):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_welcome or custom_content:
            welcome_settings.custom_content = custom_content
            welcome_settings.custom_welcome = custom_welcome
            welcome_settings.welcome_type = welcome_type.value

        else:
            welcome_settings.custom_welcome = random.choice(DEFAULT_WELCOME_MESSAGES)
            welcome_settings.welcome_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with WELC_BTN_LOCK:
            prev_buttons = (
                SESSION.query(WelcomeButtons)
                .filter(WelcomeButtons.chat_id == str(chat_id))
                .all()
            )
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = WelcomeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_welcome(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = random.choice(DEFAULT_WELCOME_MESSAGES)
    if welcome_settings and welcome_settings.custom_welcome:
        ret = welcome_settings.custom_welcome

    SESSION.close()
    return ret


def set_custom_gdbye(chat_id, custom_goodbye, goodbye_type, buttons=None):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_goodbye:
            welcome_settings.custom_leave = custom_goodbye
            welcome_settings.leave_type = goodbye_type.value

        else:
            welcome_settings.custom_leave = random.choice(DEFAULT_GOODBYE_MESSAGES)
            welcome_settings.leave_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with LEAVE_BTN_LOCK:
            prev_buttons = (
                SESSION.query(GoodbyeButtons)
                .filter(GoodbyeButtons.chat_id == str(chat_id))
                .all()
            )
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = GoodbyeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_gdbye(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = random.choice(DEFAULT_GOODBYE_MESSAGES)
    if welcome_settings and welcome_settings.custom_leave:
        ret = welcome_settings.custom_leave

    SESSION.close()
    return ret


def get_welc_buttons(chat_id):
    try:
        return (
            SESSION.query(WelcomeButtons)
            .filter(WelcomeButtons.chat_id == str(chat_id))
            .order_by(WelcomeButtons.id)
            .all()
        )
    finally:
        SESSION.close()


def get_gdbye_buttons(chat_id):
    try:
        return (
            SESSION.query(GoodbyeButtons)
            .filter(GoodbyeButtons.chat_id == str(chat_id))
            .order_by(GoodbyeButtons.id)
            .all()
        )
    finally:
        SESSION.close()


def clean_service(chat_id: Union[str, int]) -> bool:
    try:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if chat_setting:
            return chat_setting.clean_service
        return False
    finally:
        SESSION.close()


def set_clean_service(chat_id: Union[int, str], setting: bool):
    with CS_LOCK:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if not chat_setting:
            chat_setting = CleanServiceSetting(chat_id)

        chat_setting.clean_service = setting
        SESSION.add(chat_setting)
        SESSION.commit()


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Welcome).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)

        with WELC_BTN_LOCK:
            chat_buttons = (
                SESSION.query(WelcomeButtons)
                .filter(WelcomeButtons.chat_id == str(old_chat_id))
                .all()
            )
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        with LEAVE_BTN_LOCK:
            chat_buttons = (
                SESSION.query(GoodbyeButtons)
                .filter(GoodbyeButtons.chat_id == str(old_chat_id))
                .all()
            )
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        SESSION.commit()
