import random
import threading
from typing import Union

from ReyzuRobot.modules.helper_funcs.msg_types import Types
from ReyzuRobot.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from sqlalchemy.sql.sqltypes import BigInteger

DEFAULT_WELCOME_MESSAGES = [
    "{first} disini, ayo nimbrung kawan!",  # Discord welcome messages copied
    "Kamu siap {first}. Luapkan semua unek-unekmu disini",
    "Teman-teman, {first} telah hadir.",
    "Hai {first}, muncullah, ikut nimbrung yuk.",
    "{first} datang seperti Singa pergi seperti Puma.",
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
    "Selamat datang ayo kita berbahagia!",  # Tokyo Ghoul
    "{first} telah datang, ayo kita sambut.",  # op
    "{first} Baru bergabung! Salam kenal!",  # Op
    "Hai {first} welcome",
    "Hai {first}, I love you!",  # Naruto stuff begins from here
    "{first} bergabung, ambil dulu casan!",
    "{first}! Saya Ochobot, salam kenal",
    "{first}, kali ini aku akan meminjamkanmu kekuatanku, semangatlah kawan. ",  # Kyuubi to naruto
    "{first}, welcome to grup kaga jelas ini!",  # Naruto thingies end here
    "hai {first} aku lelah, beri aku motivasi.",  # Jumanji stuff
    "Dr.{first} Arkeolog terkenal dan penjelajah internasional,\nWelcome to Jumanji!\nNasib Jumanji terserah Anda sekarang.",
    "{first}, ini tidak akan menjadi misi yang mudah. Monyet diatas memperlambat ekspedisi.",  # End of Jumanji stuff
    "Hai {first} sesakit apapun kamu, jangan pernah berharap sama manusia yah.",  # V for Vendetta
    "Makan, makan, makan dan jangan lupa makan.",  # V for Vendetta
    "Di kepala {first} ada beberapa ide menarik, ayo bagikan ide-idemu disini.",  # V for Vendetta
    "Cintai amarahmu, bukan sangkarmu.",  # V for Vendetta
    "Cintai dirimu dulu sebelum mencintai orang lain",  # Planet of the apes
    "Dasar, akhirnya gabung juga kamu {first}.",
    "Saya kembali - {first}. Welcome.",
    "Hai {first} makanlah yang banyak biar gemuk.",
    "500-8 = ... ?",
]
DEFAULT_GOODBYE_MESSAGES = [
    "{first} akan dirindukan.",
    "{first} baru saja offline.",
    "{first} telah meninggalkan Grup.",
    "{first} telah keluar dari Grup",
    "{first} keluar dari Grup",
    "{first} meninggalkan Grup kita",
    "{first} sedang keluar dari Grup nyari jodoh.",
    "Senang mengenalmu, {first}!",
    "Waktu yang sinkat ya {first}.",
    "Kami berharap dapat melihat Anda lagi segera, {first}.",
    "Aku ingin mengucapkan selamat tinggal, {first}.",
    "Goodbye {first}! Tebak siapa yang akan merindukanmu :')",
    "Goodbye {first}! Akan sepi tanpamu.",
    "Tolong jangan tinggalkan aku sendirian di tempat ini, {first}!",
    "Semoga berhasil menemukan teman-teman yang lebih baik dari kami, {first}!",
    "Kamu tahu kami akan merindukanmu {first}. Goodbye.",
    "Congratulations, {first}! Anda resmi bebas dari kekacauan ini.",
    "{first}. Anda adalah kawan yang layak diperjuangkan.",
    "Anda pergi, {first}? Yare Yare Daze.",
    "Goodbye {first}",
    "{first} pergi ke luar Grup!",
    "Tanya lagi nanti",
    "Memikirkan diri sendiri",
    "Pertanyaan otoritas, kenapa kamu pergi {firtst}",
    "{first} kamu mau pergi kemana?",
    "Don't leave {first}, masih banyak cerita disini.",
    "Menyerah!",
    "Menikah dan bereproduksi",
    "Tetap tidur",
    "Bangun",
    "Lihat ke la luna",
    "Goodbye",
    "Temuilah orang asing tanpa prasangka buruk",
    "Seorang pria yang digantung tidak akan memberimu keberuntungan hari ini",
    "Apa yang ingin kamu lakukan hari ini?",
    "Kamu gelap di dalam",
    "Pernahkah Anda melihat pintu keluar?",
    "Dapatkan bayi kucing, peliharaan itu akan menghibur Anda.",
    "Jodohmu ada di Grup lain.",
    "Anda salah memainkannya, beri saya pengontrolnya",
    "Jangan percaya meskipun dia orang baik",
    "Hidup untuk mati.",
    "Ketika hidup mencari sesuatu yang baik!",
    "Yah, kukira kita teman",
    "Saya ketiduran!",
    "Semoga masalahmu cepat terselesaikan",
    "Kehidupan yang sekarang apakah sudah mulai membaik?",
    "Selalu lihat sisi baiknya",
    "Berbahaya untuk pergi sendirian",
    "Anda tidak akan pernah dimaafkan",
    "Anda tidak memiliki siapa pun untuk disalahkan kecuali diri Anda sendiri",
    "Hanya seorang pejuang",
    "Gunakan bom dengan bijak",
    "Tidak ada yang tahu masalah yang Anda lihat",
    "Anda terlihat gemuk, Anda harus lebih banyak berolahraga",
    "Ikuti zebranya",
    "Mengapa begitu sepi?",
    "Iblis yang menyamar",
    "{firts} pergi ke luar",
    "Goodbye, semoga harimu menyenangkan.",
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
