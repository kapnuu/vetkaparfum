from datetime import datetime
from flask import render_template, redirect, url_for, flash, g, send_from_directory, request, session
from vetka import app, models, db, tagcloud, security
from sqlalchemy import and_, or_, desc
import random
import jinja2
from os import path, environ

g_tags = None


def increment_tag_count(cat, tag_list):
    t = tag_list.get(cat)
    if t is None:
        tag_list[cat] = 1
    else:
        tag_list[cat] += 1


def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq


jinja2.filters.FILTERS['shuffle'] = filter_shuffle


def find_good(good_id, allow_deleted=False):
    gg = None
    if good_id.isdigit():
        gg = models.Good.query.filter(models.Good.id == good_id).first()
    if gg is None:
        gg = models.Good.query.filter(models.Good.name_en == good_id).first()
    if gg.deleted and not allow_deleted:
        gg = None
    return gg


@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')


@app.before_request
def before_request():
    global g_tags
    if g_tags is None:
        print('creating tag cloud')
        tag_list = {}
        goods = models.Good.query.filter(models.Good.deleted == False)
        for gg in goods:
            gg.category.primary = True
            increment_tag_count(gg.category, tag_list)
            for tag in gg.tags:
                increment_tag_count(tag, tag_list)
        g_tags = tagcloud.tagcloud(tag_list)
    g.tags = g_tags
    g.vk_group = environ.get('VK_GROUP')
    g.yandexCounter = environ.get('YANDEX_COUNTER')


@app.route('/')
def home():
    global g_tags
    g_tags = None

    goods = models.Good.query.filter(models.Good.deleted == False).order_by(desc(models.Good.priority))

    return render_template(
        'index.html',
        title='Натуральная косметика',
        year=datetime.now().year,
        goods=goods
    )


@app.route('/login', methods=['POST'])
def login():
    salt = '123456'
    password = request.form['password']
    if password is not None:
        passw_hash = security.encrypt(password, salt)
        if passw_hash == '4fc728b424b618c856ddac8f3854bd048247c06f92b851a3c728a83ca2afba6c' and \
                        request.form['username'] == 'vetka':
            session['logged_in'] = True
        else:
            flash('Invalid login or password!', category='error')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/good/<good_id>')
def good(good_id):
    allow_deleted = session.get('logged_in') is not None;
    gg = find_good(good_id, allow_deleted)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))

    title = gg.product
    if gg.name:
        title = title + ' "' + gg.name + '"'
    return render_template(
        'good.html',
        title=title,
        year=datetime.now().year,
        good=gg,
        good_page=True
    )


@app.route('/tag/<tag_id>')
@app.route('/category/<tag_id>')
def category(tag_id):
    cat = models.Category.query.filter_by(name_en=tag_id).first()
    if cat is None:
        cat = models.Category.query.filter_by(name=tag_id).first()
    if cat is None:
        flash('Category <strong>' + tag_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))

    goods = list(models.Good.query.filter(and_(cat.id == models.Good.category_id, models.Good.deleted == False)))
    if cat.goods2:
        goods.extend([x for x in cat.goods2 if not x.deleted])
    goods.sort(key=lambda x: x.priority, reverse=True)

    return render_template(
        'category.html',
        title=cat.name,
        year=datetime.now().year,
        goods=goods,
        category=cat
    )


def unauthorized():
    if not session.get('logged_in'):
        flash('You must be authorized for this action.', category='error')
        return True


@app.route('/deleted-goods')
def grave():
    if unauthorized():
        return redirect(url_for('home'))

    goods = models.Good.query.filter(models.Good.deleted).order_by(desc(models.Good.priority))
    return render_template(
        'deleted.html',
        title='Натуральная косметика',
        year=datetime.now().year,
        goods=goods if goods.first() is not None else None
    )


@app.route('/good/restore/<good_id>')
def restore(good_id):
    if unauthorized():
        return redirect(url_for('home'))

    gg = find_good(good_id, True)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))
    if not gg.deleted:
        flash('Good <strong>' + good_id + '</strong> not deleted. Nothing to restore.', category='error')
        return redirect(url_for('home'))

    global g_tags
    g_tags = None

    gg.deleted = False
    # db.session.add(gg)
    db.session.commit()
    # db.session.expunge(gg)
    flash('Good <a href=' + url_for('good', good_id=good_id) + '>' + good_id + '</a> restored. <a href=' +
          url_for('delete', good_id=good_id) + '>Delete?</a>', category='success')

    return redirect(url_for('home'))


@app.route('/good/delete/<good_id>')
def delete(good_id):
    if unauthorized():
        return redirect(url_for('home'))

    gg = find_good(good_id, True)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))
    if gg.deleted:
        flash('Good <strong>' + good_id + '</strong> already deleted.', category='error')
        return redirect(url_for('home'))

    global g_tags
    g_tags = None

    gg.deleted = True
    # db.session.add(gg)
    db.session.commit()
    # db.session.expunge(gg)
    flash('Good <a href=' + url_for('good', good_id=good_id) + '>' + good_id + '</a> deleted. <a href=' +
          url_for('restore', good_id=good_id) + '>Restore?</a>', category='success')
    return redirect(url_for('home'))
