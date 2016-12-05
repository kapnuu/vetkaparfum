﻿from datetime import datetime
from flask import render_template, redirect, url_for, flash, g, send_from_directory, request, session
from vetka import app, models, db, tagcloud, security, forms
from sqlalchemy import and_, or_, desc
import random
import string
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
    if gg is not None and gg.deleted and not allow_deleted:
        gg = None
    return gg


def find_tag(tag_id, allow_deleted=False):
    tt = None
    if tag_id.isdigit():
        tt = models.Category.query.filter(models.Category.id == tag_id).first()
    if tt is None:
        tt = models.Category.query.filter(models.Category.name_en == tag_id).first()
    if tt is not None and tt.deleted and not allow_deleted:
        tt = None
    return tt


def find_tag_not_cat(tag_id, allow_deleted=False):
    tt = None
    if tag_id.isdigit():
        tt = models.Category.query.filter(and_(models.Category.id == tag_id, models.Category.primary == False)).first()
    if tt is None:
        tt = models.Category.query.filter(
            and_(models.Category.name_en == tag_id, models.Category.primary == False)).first()
    if tt is not None and tt.deleted and not allow_deleted:
        tt = None
    return tt


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
            # gg.category.primary = True
            increment_tag_count(gg.category, tag_list)
            for tag in gg.tags:
                if not tag.deleted:
                    increment_tag_count(tag, tag_list)
        g_tags = tagcloud.tagcloud(tag_list)
    g.tags = g_tags
    g.vk_group = environ.get('VK_GROUP')
    g.yandexCounter = environ.get('YANDEX_COUNTER')


@app.route('/good')
def home2():
    return home()


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
    username = request.form['username']
    password = request.form['password']
    if username is not None and password is not None:
        if app.config.get('DEVELOPMENT'):
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            password_hash = security.encrypt(password, salt)
            session['logged_in'] = True
            print('username: %s salt: %s hash: %s' % (username, salt, password_hash))
        else:
            salt = app.config.get('ADMIN_SALT')
            true_username = app.config.get('ADMIN_USERNAME')
            true_password = app.config.get('ADMIN_PASSWORD')
            if salt is not None and true_username is not None and true_password is not None:
                password_hash = security.encrypt(password, salt)
                if password_hash == true_password and username == true_username:
                    session['logged_in'] = True
                else:
                    flash('Invalid login or password!', category='error')
            else:
                flash('Nobody can do this. Nobody.', category='error')
    else:
        flash('Invalid login or password!', category='error')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/good/<good_id>')
def good(good_id):
    allow_deleted = session.get('logged_in') is not None
    gg = find_good(good_id, allow_deleted)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))

    see_also = [t for t in gg.tags if t.description]

    title = gg.product
    if gg.name:
        title = title + ' "' + gg.name + '"'
    return render_template(
        'good.html',
        title=title,
        year=datetime.now().year,
        good=gg,
        see_also=see_also,
        good_page=True
    )


@app.route('/tag/<tag_id>')
@app.route('/category/<tag_id>')
def category(tag_id):
    allow_deleted = session.get('logged_in') is not None
    cat = find_tag(tag_id, allow_deleted)
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


@app.route('/tag')
@app.route('/category')
def tag_list():
    if unauthorized():
        return redirect(url_for('home'))

    tags = models.Category.query.filter(
        and_(models.Category.deleted == False, models.Category.primary == False)).order_by(models.Category.name)

    return render_template(
        'tags.html',
        title='Натуральная косметика',
        year=datetime.now().year,
        tags=tags
    )


def unauthorized():
    if not session.get('logged_in'):
        flash('You must be authorized for this action.', category='error')
        return True


@app.route('/grave')
def grave():
    if unauthorized():
        return redirect(url_for('home'))

    goods = models.Good.query.filter(models.Good.deleted).order_by(desc(models.Good.priority))

    tags = models.Category.query.filter(models.Category.deleted).order_by(models.Category.name)

    return render_template(
        'deleted.html',
        title='Натуральная косметика',
        year=datetime.now().year,
        goods=goods if goods.first() is not None else None,
        tags=tags if tags.first() is not None else None
    )


@app.route('/good/restore/<good_id>')
def good_restore(good_id):
    if unauthorized():
        return redirect(url_for('home'))

    gg = find_good(good_id, True)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))
    if not gg.deleted:
        flash('Good <a href=' + url_for('good', good_id=good_id) + '>' + good_id +
              '</a> not deleted. Nothing to restore.', category='error')
        return redirect(url_for('home'))

    global g_tags
    g_tags = None

    gg.deleted = False
    db.session.commit()
    flash('Good <a href=' + url_for('good', good_id=good_id) + '>' + good_id + '</a> restored. <a href=' +
          url_for('good_delete', good_id=good_id) + '>Delete?</a>', category='success')

    return redirect(url_for('home'))


@app.route('/good/delete/<good_id>')
def good_delete(good_id):
    if unauthorized():
        return redirect(url_for('home'))

    gg = find_good(good_id, True)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))
    if gg.deleted:
        flash('Good <a href=' + url_for('good', good_id=good_id) + '>' + good_id + '</a> already deleted.',
              category='error')
        return redirect(url_for('home'))

    global g_tags
    g_tags = None

    gg.deleted = True
    db.session.commit()
    flash('Good <a href=' + url_for('good', good_id=good_id) + '>' + good_id + '</a> deleted. <a href=' +
          url_for('good_restore', good_id=good_id) + '>Restore?</a>', category='success')
    return redirect(url_for('home'))


@app.route('/good/add', methods=['GET', 'POST'])
def good_add():
    if unauthorized():
        return redirect(url_for('home'))

    form = forms.AddGoodForm()
    if form.validate_on_submit():
        product = form.product.data
        name = form.name.data
        name_en = form.name_en.data
        description = form.description
        image = form.image.data
        cat = models.Category.query.filter(models.Category.id == form.category.data).first()
        price = form.price.data
        priority = form.priority.data
        tags = [models.Category.query.filter(models.Category.id == t_id).first() for t_id in form.tags.data]

        new_good = models.Good(product=product, name=name, name_en=name_en, description=description, image=image,
                               category=cat, price=price, priority=priority, tags=tags)

        global g_tags
        g_tags = None

        db.session.add(new_good)
        db.session.commit()
        flash('New good <a href=' + url_for('good', good_id=new_good.name_en) + '>' + new_good.name_en + '</a> added.',
              category='success')

        return redirect(url_for('home'))

    return render_template('add-good.html', form=form, good_page=True)


@app.route('/good/edit/<good_id>', methods=['GET', 'POST'])
def good_edit(good_id):
    if unauthorized():
        return redirect(url_for('home'))

    gg = find_good(good_id, False)
    if gg is None:
        flash('Good <strong>' + good_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))

    form = forms.EditGoodForm()
    if form.validate_on_submit():
        gg.product = form.product.data
        gg.name = form.name.data
        gg.name_en = form.name_en.data
        gg.description = form.description.data
        gg.image = form.image.data
        gg.cat = models.Category.query.filter(models.Category.id == form.category.data).first()
        gg.price = form.price.data
        gg.priority = form.priority.data
        gg.tags = [models.Category.query.filter(models.Category.id == t_id).first() for t_id in form.tags.data]

        db.session.commit()
        flash('Good <a href=' + url_for('good', good_id=gg.name_en) + '>' + gg.name_en + '</a> updated.',
              category='success')

        return redirect(url_for('home'))

    form.id.data = gg.id
    form.product.data = gg.product
    form.name.data = gg.name
    form.name_en.data = gg.name_en
    form.description.data = gg.description
    form.image.data = gg.image
    form.category.data = gg.category.id
    form.price.data = gg.price
    form.priority.data = gg.priority
    form.tags.data = [t.id for t in gg.tags]

    return render_template('add-good.html', form=form, good_page=True)


@app.route('/tag/delete/<tag_id>')
def tag_delete(tag_id):
    if unauthorized():
        return redirect(url_for('home'))

    tt = find_tag_not_cat(tag_id, True)
    if tt is None:
        flash('Tag <strong>' + tag_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))
    if tt.deleted:
        flash('Tag <a href=' + url_for('tag_list', tag_id=tag_id) + '>' + tag_id + '</a> already deleted.',
              category='error')
        return redirect(url_for('home'))

    global g_tags
    g_tags = None

    tt.deleted = True
    db.session.commit()
    flash('Tag <a href=' + url_for('tag_list', tag_id=tag_id) + '>' + tag_id + '</a> deleted. <a href=' +
          url_for('tag_restore', tag_id=tag_id) + '>Restore?</a>', category='success')
    return redirect(url_for('home'))


@app.route('/tag/restore/<tag_id>')
def tag_restore(tag_id):
    if unauthorized():
        return redirect(url_for('home'))

    tt = find_tag_not_cat(tag_id, True)
    if tt is None:
        flash('Tag <strong>' + tag_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))
    if not tt.deleted:
        flash('Tag <a href=' + url_for('tag_list', tag_id=tag_id) + '>' + tag_id +
              '</a> not deleted. Nothing to restore.', category='error')
        return redirect(url_for('home'))

    global g_tags
    g_tags = None

    tt.deleted = False
    db.session.commit()
    flash('Tag <a href=' + url_for('tag_list', tag_id=tag_id) + '>' + tag_id + '</a> restored. <a href=' +
          url_for('tag_delete', tag_id=tag_id) + '>Delete?</a>', category='success')

    return redirect(url_for('home'))


@app.route('/tag/add', methods=['GET', 'POST'])
def tag_add():
    if unauthorized():
        return redirect(url_for('home'))

    form = forms.AddTagForm()
    if form.validate_on_submit():
        name = form.name.data
        name_en = form.name_en.data
        description = form.description.data

        new_tag = models.Category(name=name, name_en=name_en,description=description)

        db.session.add(new_tag)
        db.session.commit()
        flash('New tag <a href=' + url_for('category', tag_id=new_tag.name_en) + '>#' + new_tag.name + '</a> added.',
              category='success')

        return redirect(url_for('home'))

    return render_template('add-tag.html', form=form, good_page=True)


@app.route('/tag/edit/<tag_id>', methods=['GET', 'POST'])
def tag_edit(tag_id):
    if unauthorized():
        return redirect(url_for('home'))

    tt = find_tag_not_cat(tag_id, True)
    if tt is None:
        flash('Tag <strong>' + tag_id + '</strong> not found.', category='error')
        return redirect(url_for('home'))

    form = forms.EditTagForm()
    if form.validate_on_submit():
        tt.name = form.name.data
        tt.name_en = form.name_en.data
        tt.description = form.description.data

        db.session.commit()
        flash('Tag <a href=' + url_for('category', tag_id=tt.name_en) + '>#' + tt.name + '</a> updated.',
              category='success')
        return redirect(url_for('home'))

    form.id.data = tt.id
    form.name.data = tt.name
    form.name_en.data = tt.name_en
    form.description.data = tt.description

    return render_template('add-tag.html', form=form, good_page=True)


@app.route('/fix/<fix_id>')
def fix(fix_id):
    if unauthorized():
        return redirect(url_for('home'))

    if fix_id == 'cat-primary':
        global g_tags
        g_tags = None

        for cat in models.Category.query.all():
            cat.primary = cat.name_en in ['face', 'body', 'hair', 'parfum', 'nails']

        db.session.commit()
        flash('Fix <strong>' + fix_id + '</strong> applied.', category='success')
    else:
        flash('Fix <strong>' + fix_id + '</strong> not found.', category='error')

    return redirect(url_for('home'))
