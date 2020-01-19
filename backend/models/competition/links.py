from backend.models.base import db, TABLE_COMPETITION_LEAD, TABLE_COMPETITION_FOLLOW, \
    TABLE_COMPETITION_COUPLE, TABLE_COMPETITION_ADJUDICATOR


competition_lead_table = db.Table(
    TABLE_COMPETITION_LEAD, db.Model.metadata,
    db.Column("competition_id", db.Integer,
              db.ForeignKey("competition.competition_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("dancer_id", db.Integer, db.ForeignKey("dancer.dancer_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("competition_id", "dancer_id", name="_competition_lead_uc")
)


competition_follow_table = db.Table(
    TABLE_COMPETITION_FOLLOW, db.Model.metadata,
    db.Column("competition_id", db.Integer,
              db.ForeignKey("competition.competition_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("dancer_id", db.Integer, db.ForeignKey("dancer.dancer_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("competition_id", "dancer_id", name="_competition_follow_uc")
)


competition_couple_table = db.Table(
    TABLE_COMPETITION_COUPLE, db.Model.metadata,
    db.Column("competition_id", db.Integer,
              db.ForeignKey("competition.competition_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("couple_id", db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("competition_id", "couple_id", name="_competition_couple_uc")
)


competition_adjudicator_table = db.Table(
    TABLE_COMPETITION_ADJUDICATOR, db.Model.metadata,
    db.Column("competition_id", db.Integer,
              db.ForeignKey("competition.competition_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("adjudicator_id", db.Integer,
              db.ForeignKey("adjudicator.adjudicator_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("competition_id", "adjudicator_id", name="_competition_adjudicator_uc")
)
