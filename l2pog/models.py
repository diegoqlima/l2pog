from django.db import models

# Create your models here.
class Useradmin(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    username = models.CharField(max_length=30, db_column='username')
    class Meta:
        db_table = u'auth_user'
    def __unicode__(self):
        return self.username

class User(models.Model):
    iduser = models.IntegerField(primary_key=True, db_column='idUser')
    username = models.CharField(db_column='userName', max_length=45)
    usermail = models.CharField(db_column='userMail', max_length=45)
    userregistration = models.DateTimeField(db_column='userRegistrationDate')
    class Meta:
        db_table = u'user'
    def __unicode__(self):
        return self.username

class Vote(models.Model):
    idvote = models.IntegerField(primary_key=True, db_column='idVote')
    datevote = models.DateTimeField(db_column='dateVote')
    ipvote = models.IPAddressField(db_column='ipVote')
    iduser = models.ForeignKey(User, db_column='idUser')
    class Meta:
        db_table = u'vote'
    def __unicode__(self):
        return self.ipvote

class Notice(models.Model):
    idnotice = models.IntegerField(primary_key=True, db_column='idNotice')
    subject = models.CharField(max_length=100, db_column='subject')
    text = models.TextField(db_column='text')
    date = models.DateTimeField(db_column='date')
    author = models.ForeignKey(Useradmin)
    class Meta:
        db_table = u'notice'
    def __unicode__(self):
        return self.subject

class Contact(models.Model):
    idcontact = models.IntegerField(primary_key=True, db_column='idContact')
    name = models.CharField(max_length=50, db_column='name')
    email = models.CharField(max_length=100, db_column='email')
    subject = models.CharField(max_length=100, db_column='subject')
    message = models.TextField(db_column='message')
    date = models.DateTimeField(db_column='date')
    class Meta:
        db_table = u'contact'
    def __unicode__(self):
        return self.name

class Link(models.Model):
    idlink = models.IntegerField(primary_key=True, db_column='idLink')
    urllink = models.TextField(db_column='urlLink')
    class Meta:
        db_table = u'link'
    def __unicode__(self):
        return self.urllink

class Accounts(models.Model):
    login = models.CharField(max_length=45, db_column='login', primary_key=True)
    password = models.CharField(max_length=45, db_column='password')
    iduser = models.ForeignKey(User, db_column='idUser')
    class Meta:
        db_table = u'accounts'
    def __unicode__(self):
        return self.login

class Characters(models.Model):
    charid = models.IntegerField(primary_key=True, db_column='charId')
    charname = models.CharField(db_column='char_name', max_length=35)
    accountname = models.CharField(db_column='account_name', max_length=45)
    class Meta:
        db_table = u'characters'
    def __unicode__(self):
        return self.charname

class Items(models.Model):
    ownerid = models.IntegerField(db_column='owner_id')
    objectid = models.IntegerField(primary_key=True, db_column='object_id')
    itemid = models.IntegerField(db_column='item_id')
    count = models.IntegerField(db_column='count')
    enchantlevel = models.IntegerField(db_column='enchant_level')
    loc = models.CharField(db_column='loc', max_length=10)
    locdata = models.IntegerField(db_column='loc_data')
    timeuse = models.IntegerField(db_column='time_of_use')
    customtype1 = models.IntegerField(db_column='custom_type1')
    customtype2 = models.IntegerField(db_column='custom_type2')
    manaleft = models.DecimalField(max_digits=5, decimal_places=0, db_column='mana_left')
    time = models.DecimalField(max_digits=13, decimal_places=0, db_column='time')
    class Meta:
        db_table = u'items'
    def __unicode__(self):
        return self.objectid