#pragma once

#include "service.h"
#include "cos.h"
#include <QWidget>
#include <QListWidget>
#include <QBoxLayout>
#include <QPushButton>
#include <QFormLayout>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QLayout>
#include <QTextBlock>
#include <QTableWidget>
#include <set>
#include <QSlider>
#include <QPainter>
#include <QListView>
#include "observer.h"
#include "MyList.h"

class CosGUI : public QWidget, public Observer {
private:
    Cos& rep;
    Service& srv;
    QHBoxLayout*  cos_main_layout = new QHBoxLayout;

    QListWidget* cos_lst;

    QLineEdit* lne_cos;
    QPushButton* add_to_wish;
    QPushButton* empty_wish;
    QPushButton* random_add;
    QPushButton* export_cos;
    QPushButton* help_button;

    void initGUI();
    void connectSignals();
    void reloadTurs(vector<Turism> turs);
    void update() override {
        reloadTurs(rep.get_all());
    }
public:
    CosGUI(Cos& rep, Service& srv) : srv{ srv }, rep{ rep } {
        rep.addObs(this);
        initGUI();
        connectSignals();
        reloadTurs(rep.get_all());
    }

    ~CosGUI() {
        rep.rmObs(this);
    }
};


class PaintGUI : public QWidget, public Observer {
private:
    Cos& rep;
public:
    PaintGUI(Cos& rep) :rep{ rep } {
        rep.addObs(this);
    }

    void paintEvent(QPaintEvent*) override {
        QPainter p{ this };
        int x;
        int y;
        for (auto& it : rep.get_all()) {
            x = rand() % 400 + 1;
            y = rand() % 400 + 1;
            
            QRectF target(x, y, 100, 94);
            QRectF source(0, 0, 732, 720);
            QImage image("ucluj.jpg");

            p.drawImage(target, image, source);
        }
    }

    void update() override {
        repaint();
    }

    ~PaintGUI() {
        rep.rmObs(this);
    }
};

class GUI : public QWidget {
private:
    vector<Turism> act_list;
    Service srv;
    Cos rep;
    QListWidget* lst = new QListWidget;

    QListView* lst_view = new QListView;
    MyList* model;

    vector<CosGUI*> rcp;
    vector<PaintGUI*> pg;

    QHBoxLayout* lyMain = new QHBoxLayout;
    QPushButton* btnSortDenumire;
    QPushButton* btnSortDestinatie;
    QPushButton* btnSortTP;
    QPushButton* btnFilterPret;
    QPushButton* btnFilterDestinatie;
    QPushButton* btn_add;
    QPushButton* btn_mod;
    QPushButton* btn_del;
    QPushButton* btn_undo;
    QPushButton* btn_cos_mst;
    QPushButton* btn_cos_rdonly;
    QPushButton* btn_reset;
    QLineEdit* txtDenumire;
    QLineEdit* txtDestinatie;
    QLineEdit* txtTip;
    QLineEdit* txtPret;
    QLineEdit* txtFilt;
    QListWidget* cos_lst;
    QSlider* lmn;

    QWidget* opt_but;
    QVBoxLayout* lay_opt;

    vector<QPushButton*> subst_but;

    int lb_index;
    void init_GUI();
    void connectSignalsSlots();
    void reloadList(vector<Turism>& turs);
    void updateBut(vector<Turism>& all);

    void addTur();
    void delTur();
    void updTur();
    void undoTur();

    void reset_form();
public:
    GUI(Service& srv) : srv{ srv } {
        init_GUI();
        model = new MyList{ srv.get_all_ent() };
        lst_view->setModel(model);
        connectSignalsSlots();
        reloadList(srv.get_all_ent());
        act_list = srv.get_all_ent();
        updateBut(srv.get_all_ent());
        rcp.push_back(new CosGUI{ rep,srv });
        rcp[0]->show();
        pg.push_back(new PaintGUI{ rep });
        pg[0]->show();
    }

    void paintEvent(QPaintEvent*) override {
        QPainter p{ this };
        p.drawEllipse(QPointF(20, 20), 20, 20);
        p.drawEllipse(QPointF(this->width() - 20, this->height() - 20), 20, 20);
        p.drawEllipse(QPointF(this->width() - 20, 20), 20, 20);
        p.drawEllipse(QPointF(20, this->height() - 20), 20, 20);
    }
};
