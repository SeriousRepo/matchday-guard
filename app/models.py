from django.db import models


class Competition(models.Model):
    internal_identifier = models.IntegerField(unique=True)
    external_identifier = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    area_id = models.CharField(max_length=100)
    year = models.IntegerField()


class Team(models.Model):
    internal_identifier = models.IntegerField(unique=True)
    external_identifier = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    stadium = models.CharField(max_length=100)


class Person(models.Model):
    internal_identifier = models.IntegerField(unique=True)
    external_identifier = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=30)
    position = models.CharField(max_length=50, null=True)
    shirt_number = models.IntegerField(null=True)
    external_team_identifier = models.IntegerField(null=True)


class Player(models.Model):
    internal_identifier = models.IntegerField(unique=True)
    internal_person_identifier = models.IntegerField()


class Match(models.Model):
    external_identifier = models.IntegerField(unique=True)
    home_team_external_id = models.IntegerField(null=True)
    away_team_external_id = models.IntegerField(null=True)
    home_team_goals = models.IntegerField(null=True)
    away_team_goals = models.IntegerField(null=True)
