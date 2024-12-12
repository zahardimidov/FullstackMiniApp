from database.session import Base
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(BigInteger, nullable=False, primary_key=True)
    username = mapped_column(String(50), default="Guest")

    registered_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __str__(self) -> str:
        return self.username


class UserRef(Base):
    __tablename__ = 'userref'

    referral_id = mapped_column(ForeignKey('users.id'), primary_key=True)
    referral: Mapped['User'] = relationship(
        'User',
        foreign_keys=[referral_id],
        backref='referrals',
        primaryjoin='UserRef.referral_id == User.id',
        lazy='subquery'
    )

    referrer_id = mapped_column(ForeignKey('users.id'), primary_key=True)
    referrer: Mapped['User'] = relationship(
        'User',
        foreign_keys=[referrer_id],
        backref='referrers',
        primaryjoin='UserRef.referrer_id == User.id',
        lazy='subquery'
    )

    def __str__(self):
        return f'{self.referral.username} - {self.referrer.username}'
