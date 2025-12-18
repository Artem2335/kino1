from sqlalchemy import Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class Review(Base):
    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)  # рейтинг в рецензии (1-5)
    approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, movie_id={self.movie_id})"
