from datetime import datetime
from flask import render_template, redirect, url_for, flash, g, send_from_directory
from vetka import app, models, db, tagcloud
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


@app.route('/good/<good_id>')
def good(good_id):
    gg = None
    if good_id.isdigit():
        gg = models.Good.query.filter_by(id=good_id).first()
    if gg is None:
        gg = models.Good.query.filter_by(name_en=good_id).first()
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
        goods.extend([x for x in cat.goods2 if x.deleted == False])
    goods.sort(key=lambda x: x.priority, reverse=True)

    return render_template(
        'category.html',
        title=cat.name,
        year=datetime.now().year,
        goods=goods,
        category=cat
    )
