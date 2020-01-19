from backend.models.base import db, TABLE_HEAT_COUPLE


heat_couple_table = db.Table(
    TABLE_HEAT_COUPLE, db.Model.metadata,
    db.Column("heat_id", db.Integer, db.ForeignKey("heat.heat_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("couple_id", db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint("heat_id", "couple_id", name="_heat_couple_uc")
)
