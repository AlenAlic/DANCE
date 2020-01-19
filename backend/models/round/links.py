from backend.models.base import db, TABLE_ROUND_DANCE, TABLE_ROUND_COUPLE


round_dance_table = db.Table(
    TABLE_ROUND_DANCE, db.Model.metadata,
    db.Column("round_id", db.Integer, db.ForeignKey("round.round_id",  onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("dance_id", db.Integer, db.ForeignKey("dance.dance_id",  onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("round_id", "dance_id", name="_round_dance_uc")
)

round_couple_table = db.Table(
    TABLE_ROUND_COUPLE, db.Model.metadata,
    db.Column("round_id", db.Integer, db.ForeignKey("round.round_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("couple_id", db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("round_id", "couple_id", name="_round_couple_uc")
)
