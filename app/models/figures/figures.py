from sqlalchemy.orm import Session
from app.db.models.card_fig import CardFig
from .difficult import (
    fig1,
    fig2,
    fig3,
    fig4,
    fig5,
    fig6,
    fig7,
    fig8,
    fig9,
    fig10,
    fig11,
    fig12,
    fig13,
    fig14,
    fig15,
    fig16,
    fig17,
    fig18,
)
from .easy import fig19, fig20, fig21, fig22, fig23, fig24, fig25

FIGURE_CLASSES = {
    "Figura Difícil 1": fig1(),
    "Figura Difícil 2": fig2(),
    "Figura Difícil 3": fig3(),
    "Figura Difícil 4": fig4(),
    "Figura Difícil 5": fig5(),
    "Figura Difícil 6": fig6(),
    "Figura Difícil 7": fig7(),
    "Figura Difícil 8": fig8(),
    "Figura Difícil 9": fig9(),
    "Figura Difícil 10": fig10(),
    "Figura Difícil 11": fig11(),
    "Figura Difícil 12": fig12(),
    "Figura Difícil 13": fig13(),
    "Figura Difícil 14": fig14(),
    "Figura Difícil 15": fig15(),
    "Figura Difícil 16": fig16(),
    "Figura Difícil 17": fig17(),
    "Figura Difícil 18": fig18(),
    "Figura Fácil 4": fig19(),
    "Figura Fácil 1": fig20(),
    "Figura Fácil 2": fig21(),
    "Figura Fácil 3": fig22(),
    "Figura Fácil 5": fig23(),
    "Figura Fácil 6": fig24(),
    "Figura Fácil 7": fig25(),
}


def get_all_figures():
    return [fig for fig in FIGURE_CLASSES.values()]


def get_figure_by_id(figure_id: int, db: Session):
    return db.query(CardFig).filter(CardFig.id == figure_id).first()


def get_figure_type_by_id(figure_id: int, db: Session):
    return db.query(CardFig).filter(CardFig.id == figure_id).first().figure


def select_figure_by_his_type(type_name: str):
    return FIGURE_CLASSES.get(type_name, None)
