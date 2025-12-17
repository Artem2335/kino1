from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class Favorite(Base):
    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="favorites", foreign_keys=[movie_id])
    user: Mapped["User"] = relationship("User", back_populates="favorites", foreign_keys=[user_id])

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, movie_id={self.movie_id})"
