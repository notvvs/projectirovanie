from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String, Text, Float, Boolean, Integer,
    ForeignKey, ARRAY, TIMESTAMP, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    exchanges_count: Mapped[int] = mapped_column(Integer, default=0)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    books: Mapped[list["Book"]] = relationship(back_populates="owner")
    wishlists: Mapped[list["Wishlist"]] = relationship(back_populates="user")
    initiated_exchanges: Mapped[list["Exchange"]] = relationship(
        back_populates="initiator", foreign_keys="Exchange.initiator_id"
    )
    received_exchanges: Mapped[list["Exchange"]] = relationship(
        back_populates="owner", foreign_keys="Exchange.owner_id"
    )
    messages: Mapped[list["Message"]] = relationship(back_populates="sender")
    written_reviews: Mapped[list["Review"]] = relationship(
        back_populates="author", foreign_keys="Review.author_id"
    )
    received_reviews: Mapped[list["Review"]] = relationship(
        back_populates="target", foreign_keys="Review.target_id"
    )
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
    submitted_reports: Mapped[list["Report"]] = relationship(
        back_populates="reporter", foreign_keys="Report.reporter_id"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    author: Mapped[str] = mapped_column(String(255), index=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(20))
    genre: Mapped[Optional[str]] = mapped_column(String(50))
    condition: Mapped[str] = mapped_column(String(20))  # new, good, fair
    description: Mapped[Optional[str]] = mapped_column(Text)
    photo_urls: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner: Mapped["User"] = relationship(back_populates="books")
    exchanges: Mapped[list["Exchange"]] = relationship(
        back_populates="book", foreign_keys="Exchange.book_id"
    )

    __table_args__ = (
        CheckConstraint("condition IN ('new', 'good', 'fair')", name="check_condition"),
    )


class Wishlist(Base):
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[Optional[str]] = mapped_column(String(255))
    isbn: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="wishlists")


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(primary_key=True)
    initiator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), index=True)
    offered_book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    initiator_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    initiator: Mapped["User"] = relationship(
        back_populates="initiated_exchanges", foreign_keys=[initiator_id]
    )
    owner: Mapped["User"] = relationship(
        back_populates="received_exchanges", foreign_keys=[owner_id]
    )
    book: Mapped["Book"] = relationship(
        back_populates="exchanges", foreign_keys=[book_id]
    )
    offered_book: Mapped[Optional["Book"]] = relationship(foreign_keys=[offered_book_id])
    messages: Mapped[list["Message"]] = relationship(back_populates="exchange")
    reviews: Mapped[list["Review"]] = relationship(back_populates="exchange")

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected', 'completed', 'cancelled')",
            name="check_status"
        ),
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    content: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    exchange: Mapped["Exchange"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    exchange: Mapped["Exchange"] = relationship(back_populates="reviews")
    author: Mapped["User"] = relationship(
        back_populates="written_reviews", foreign_keys=[author_id]
    )
    target: Mapped["User"] = relationship(
        back_populates="received_reviews", foreign_keys=[target_id]
    )

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating"),
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="notifications")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    target_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    moderator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    decision: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    reporter: Mapped["User"] = relationship(
        back_populates="submitted_reports", foreign_keys=[reporter_id]
    )
    target_user: Mapped["User"] = relationship(foreign_keys=[target_user_id])
    moderator: Mapped[Optional["User"]] = relationship(foreign_keys=[moderator_id])

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'resolved', 'rejected')",
            name="check_report_status"
        ),
    )