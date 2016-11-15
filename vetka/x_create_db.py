from vetka import app, models, db
from flask import redirect, url_for, flash


@app.route('/create')
def create_db():
    gg = models.Good.query.all()
    for g in gg:
        db.session.delete(g)

    cc = models.Category.query.all()
    for c in cc:
        db.session.delete(c)

    c_face = models.Category(name='Лицо', name_en='face', primary=True)
    db.session.add(c_face)
    c_body = models.Category(name='Тело', name_en='body', primary=True)
    db.session.add(c_body)
    c_hair = models.Category(name='Волосы', name_en='hair', primary=True)
    db.session.add(c_hair)
    c_nails = models.Category(name='Ногти', name_en='nails', primary=True)
    db.session.add(c_nails)
    c_parfum = models.Category(name='Духи', name_en='parfum', primary=True)
    db.session.add(c_parfum)

    t_massage = models.Category(name='массаж', name_en='massage')
    db.session.add(t_massage)
    t_aromatherapy = models.Category(name='ароматерапия', name_en='aromatherapy')
    db.session.add(t_aromatherapy)
    t_dry_parfum = models.Category(name='твёрдые духи', name_en='dry-parfum', description='''
Твёрдые духи — это прекрасная альтернатива традиционному парфюму. Они удобны в использовании, долго держатся и очень
экономно расходуются.</article>
<article>Многогранный аромат твёрдого парфюма постепенно раскрывается на коже и держится в течение всего дня благодаря
пчелиному воску, который не дает эфирным маслам мгновенно испаряться. Такие духи очень удобно взять с собой
в путешествие — маленькая баночка легко помещается в любую сумку и её можно пронести с собой в самолёт.</article>
<article>Пользоваться твёрдым парфюмом очень легко — достаточно нанести небольшое количество продукта на зоны пульса:
на запястье, за ухо, на затылок, в локтевые ямки. В состав твёрдых духов входит масло сладкого миндаля, которое поможет
смягчить и увлажнить кожу.''')
    db.session.add(t_dry_parfum)
    t_shea = models.Category(name='масло ши', name_en='shea-butter')
    db.session.add(t_shea)
    t_cinnamon = models.Category(name='корица', name_en='cinnamon')
    db.session.add(t_cinnamon)
    t_ubtan = models.Category(name='убтан', name_en='ubtan', description='''
Убтан — это аюрведический порошок, способный одновременно заменить средство для умывания, скраб и гель для душа.
Он не только прекрасно очищает, но и тонизирует, омолаживает кожу, помогает бороться с воспалительными процессами,
прекрасно справляется с черными точками, расширенными порами и прыщами. Основные составляющие убтана — злаки, лечебные
травы, глина, а также молотые орехи, специи и семена. Для умывания нужно смешать чайную ложку убтана с чайной ложкой
воды комнатной температуры (заваривать не нужно!), нанести на влажную кожу, избегая области вокруг глаз, оставить
на пару минут и смыть теплой водой. После умывания этим средством ваша кожа станет невероятно гладной,
нежной и бархатистой!''')
    db.session.add(t_ubtan)
    t_ayurveda = models.Category(name='аюрведа', name_en='ayurveda')
    db.session.add(t_ayurveda)
    t_clay = models.Category(name='глина', name_en='clay')
    db.session.add(t_clay)
    t_patchouli = models.Category(name='пачули', name_en='patchouli')
    db.session.add(t_patchouli)
    t_mint = models.Category(name='мята', name_en='mint')
    db.session.add(t_mint)
    t_strength = models.Category(name='укрепление', name_en='strength')
    db.session.add(t_strength)
    t_orange = models.Category(name='апельсин', name_en='orange')
    db.session.add(t_orange)
    t_manicure = models.Category(name='маникюр', name_en='manicure')
    db.session.add(t_manicure)
    t_beeswax = models.Category(name='пчелиный воск', name_en='beeswax', description='''
Запечатывание ногтей воском — эффективный метод укрепления ногтей, который можно осуществить в домашних условиях.
Процедура рекомендована при ломкости, слоении ногтей, а также в качестве лечения после наращивания и гель-лака.</article>
<article>Перед тем, как приступить к запечатыванию, следует подготовить ногтевую пластину:
<ol class='brace'>
<li>снять старое покрытие;</li>
<li>сформировать необходимую длину и форму ногтя;</li>
<li>очистить ногтевую пластину от ороговевших клеток, отодвинуть кутикулу и удалить заусенцы;</li>
<li>отполировать ногти замшевым бафиком или полировочной пилкой, втереть воск в ноготь (уделяя внимание свободному краю)
и кутикулу;</li>
<li>подержать руки под струёй холодной воды.</li>
</ol>
</article>
<article>Полировать ногти рекомендуется не чаще двух раз в месяц, а вот использовать воск нужно ежедневно.</article>
<article>Пчелиный воск обладает бактерицидными, смягчающими и противовоспалительными свойствами, содержит массу полезных
веществ: каротиноиды (витамин А), минеральные вещества, смолы, прополис, бета-каротин.</article>
<article>Полностью оздоровить ногти и укрепить их удаётся через 2-3 месяца регулярного использования, а результат будет держаться
очень долго.''')
    db.session.add(t_beeswax)
    t_ylang2 = models.Category(name='иланг-иланг', name_en='ylang2')
    db.session.add(t_ylang2)
    t_scrub = models.Category(name='скраб', name_en='scrub')
    db.session.add(t_scrub)
    t_lips = models.Category(name='губы', name_en='lips')
    db.session.add(t_lips)
    t_curcuma = models.Category(name='куркума', name_en='curcuma')
    db.session.add(t_curcuma)
    t_coconut = models.Category(name='кокос', name_en='coconut')
    db.session.add(t_coconut)
    t_menthol = models.Category(name='ментол', name_en='menthol')
    db.session.add(t_menthol)
    t_bergamot = models.Category(name='бергамот', name_en='bergamot')
    db.session.add(t_bergamot)
    t_pedicure = models.Category(name='педикюр', name_en='pedicure')
    db.session.add(t_pedicure)

    g_01 = models.Good(product='Твёрдые духи', name='Мак и мята',
                       description='Яркий, сладкий аромат', category=c_parfum,
                       image='https://pp.vk.me/c637828/v637828623/10c22/u0PN6g9LZdE.jpg',
                       name_en='dry-parfum-poppy-mint', price=170, deleted=True,
                       tags=[t_aromatherapy, t_dry_parfum, t_mint, t_dry_parfum])
    db.session.add(g_01)
    g_02 = models.Good(product='Массажная плитка', name='Апельсин и корица',
                       description='Масляная массажная плитка', category=c_body,
                       image='https://pp.vk.me/c637828/v637828623/10c10/tZ-NOVCR-Mc.jpg',
                       name_en='massage-tile-orange-cinnamon', price=170, priority=models.Priority.low.value,
                       tags=[t_massage, t_aromatherapy, t_shea, t_cinnamon, t_orange])
    db.session.add(g_02)
    g_03 = models.Good(product='Убтан', name='',
                       description='Аюрведическое средство для умывания', category=c_face,
                       image='https://pp.vk.me/c637828/v637828623/10bfe/bE2NRue13AI.jpg',
                       name_en='ubtan', price='200',
                       tags=[t_ubtan, t_ayurveda, t_clay, t_curcuma])
    db.session.add(g_03)
    g_04 = models.Good(product='Твёрдые духи', name='Пачули и мята',
                       description='Древесно-травяной аромат', category=c_parfum,
                       image='https://pp.vk.me/c637828/v637828623/10bec/IejA7DpykgU.jpg',
                       name_en='dry-parfum-patchouli-mint', price=120,
                       tags=[t_dry_parfum, t_patchouli, t_mint])
    db.session.add(g_04)
    g_05 = models.Good(product='Воск для ногтей', name='Апельсин и корица', category=c_nails,
                       description='Уникальное средство для укрепления ногтей',
                       image='https://pp.vk.me/c637828/v637828623/10bda/ws7SacSSSVE.jpg',
                       name_en='nails-wax-orange-cinnamon', price=120, priority=models.Priority.high.value,
                       tags=[t_cinnamon, t_strength, t_orange, t_manicure, t_beeswax])
    db.session.add(g_05)
    g_06 = models.Good(product='Воск для кончиков волос', name='Иланг-иланг', category=c_hair,
                       description='Для секущихся кончиков',
                       image='https://pp.vk.me/c637828/v637828623/10bc8/PPTUns0EqTQ.jpg',
                       name_en='hair-wax-ylang2', price=120, priority=models.Priority.high.value,
                       tags=[t_beeswax, t_ylang2, t_coconut])
    db.session.add(g_06)
    g_07 = models.Good(product='Бомбочка для ванны', name='Апельсин и мята', category=c_body,
                       description='С кокосовым маслом и листьями мяты',
                       image='https://pp.vk.me/c637828/v637828623/10bb6/0_jjQqg_-wg.jpg',
                       name_en='bath-bomb-orange-mint', price=110, priority=models.Priority.low.value,
                       tags=[t_aromatherapy, t_clay, t_mint, t_orange])
    db.session.add(g_07)
    g_08 = models.Good(product='Масло для кутикулы', name='Иланг-иланг', category=c_nails,
                       description='С маслом кокоса и виноградной косточки',
                       image='https://pp.vk.me/c637828/v637828623/10ba4/-XnGcXQZSbU.jpg',
                       name_en='cuticle-oil-ylang2', price=70,
                       tags=[t_manicure, t_ylang2])
    db.session.add(g_08)
    g_09 = models.Good(product='Масло для бровей и ресниц', name='Репейник', category=c_face,
                       description='Для быстрого роста и укрепления бровей и ресниц',
                       image='https://pp.vk.me/c637828/v637828623/10b89/9IuwGas8Yi0.jpg',
                       name_en='eyebrow-oil-agrimony', price=70, priority=models.Priority.low.value,
                       tags=[t_strength])
    db.session.add(g_09)
    g_10 = models.Good(product='Сухой шампунь для светлых волос', name='', category=c_hair,
                       description='Сухой шампунь с эфирным маслом апельсина',
                       image='https://pp.vk.me/c637828/v637828623/10b6e/ErVbM4kQP1k.jpg',
                       name_en='dry-shampoo-blond', price=150, priority=models.Priority.low.value,
                       tags=[t_orange])
    db.session.add(g_10)
    g_11 = models.Good(product='Скраб для губ', name='Мятный шоколад', category=c_face,
                       description='Охлаждающий скраб для губ с горьким шоколадом',
                       image='https://pp.vk.me/c637828/v637828623/10b53/A0GVVoCqr1o.jpg',
                       name_en='lips-scrub-mint-chocolate', price=100, priority=models.Priority.high.value,
                       tags=[t_shea, t_mint, t_scrub, t_lips])
    db.session.add(g_11)
    g_12 = models.Good(product='Бальзам для губ', name='Цитрус и мёд', category=c_face,
                       description='„Зимний” бальзам для губ на основе пчелиного воска с добавлением мёда',
                       image='https://pp.vk.me/c637828/v637828623/10b14/y_yg61QFHJg.jpg',
                       name_en='lips-balm-citrus-honey', price=120, priority=models.Priority.high.value,
                       tags=[t_shea, t_beeswax, t_lips])
    db.session.add(g_12)
    g_13 = models.Good(product='Гейзер для педикюра', name='Куркума', category=c_nails,
                       description='Гидрофильный гейзер для ванн для ног с куркумой',
                       image='https://pp.vk.me/c836228/v836228623/c6a4/IoqFZCU-S0U.jpg',
                       name_en='geyser-curcuma', price=70,
                       tags=[t_curcuma, t_coconut, t_pedicure])
    db.session.add(g_13)
    g_14 = models.Good(product='Гейзер для педикюра', name='Кокос', category=c_nails,
                       description='Гидрофильный гейзер для ванн для ног с кокосовым маслом',
                       image='https://pp.vk.me/c836228/v836228623/c6ae/SO9sve1oEuA.jpg',
                       name_en='geyser-coconut', price=70,
                       tags=[t_curcuma, t_coconut, t_pedicure])
    db.session.add(g_14)
    g_15 = models.Good(product='Скраб для тела', name='Ментол и кокос', category=c_body,
                       description='Охлаждающий сахарно-солевой скраб для тела с ментолом и кокосовой стружкой',
                       image='https://pp.vk.me/c836228/v836228623/c6b8/8x-MB-KXgds.jpg',
                       name_en='scrub-menthol-coconut', price=200,
                       tags=[t_scrub, t_menthol, t_coconut])
    db.session.add(g_15)
    g_16 = models.Good(product='Твёрдые духи в кулонах', category=c_parfum,
                       description='Твёрдые духи в кулонах с ароматом на ваш выбор',
                       image='https://pp.vk.me/c836228/v836228623/c6c2/G2pXMNIb5VE.jpg',
                       name_en='dry-parfum-pendant', price=200,
                       tags=[t_dry_parfum, t_aromatherapy, t_patchouli])
    db.session.add(g_16)
    g_17 = models.Good(product='Охлаждающий бальзам для ног', name='Бергамот и ментол', category=c_body,
                       description='Охлаждающий бальзам для ног с кристаллическим ментолом',
                       image='https://pp.vk.me/c836228/v836228623/e08d/aEKgq-ut3LY.jpg',
                       name_en='feet-balm', price=120,
                       tags=[t_bergamot, t_menthol, t_pedicure])
    db.session.add(g_17)
    db.session.commit()

    flash('New DB created', category='success')

    global g_tags
    g_tags = None

    return redirect(url_for('home'))
