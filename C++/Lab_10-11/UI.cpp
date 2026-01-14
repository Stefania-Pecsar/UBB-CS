#include "UI.h"

void GUI::init_GUI() {
    setLayout(lyMain);

    QWidget* w_left = new QWidget;
    QVBoxLayout* l_left = new QVBoxLayout;
    w_left->setLayout(l_left);

    lst_view->setUniformItemSizes(true);

    l_left->addWidget(lst_view);

    QWidget* wdg = new QWidget;
    QHBoxLayout* lay = new QHBoxLayout;
    wdg->setLayout(lay);
    btnSortDenumire = new QPushButton("Sort by Denumire");
    btnSortDestinatie = new QPushButton("Sort by Destinatie");
    btnSortTP = new QPushButton("Sort by Tip+Pret");
    lay->addWidget(btnSortDenumire);
    lay->addWidget(btnSortDestiantie);
    lay->addWidget(btnSortTP);

    l_left->addWidget(wdg);

    QWidget* form_filt = new QWidget;
    QFormLayout* form_filt_lay = new QFormLayout;
    form_filt->setLayout(form_filt_lay);

    QLabel* lbl_filt = new QLabel;
    txtFilt = new QLineEdit;

    form_filt_lay->addRow(lbl_filt, txtFilt);

    l_left->addWidget(form_filt);

    QWidget* flt_btn = new QWidget;
    QHBoxLayout* flt_lay = new QHBoxLayout;
    flt_btn->setLayout(flt_lay);

    btnFilterPret = new QPushButton("Filter by pret");
    btnFilterDestinatie = new QPushButton("Filter by destinatie");
    btn_reset = new QPushButton("Reset order");

    flt_lay->addWidget(btn_reset);
    flt_lay->addWidget(btnFilterDestinatie);
    flt_lay->addWidget(btnFilterPret);

    l_left->addWidget(flt_btn);

    lyMain->addWidget(w_left);

    //form pentru detalii
    QWidget* w_right = new QWidget;
    QVBoxLayout* lay_right = new QVBoxLayout;
    w_right->setLayout(lay_right);

    QWidget* form = new QWidget;
    QFormLayout* lay_form = new QFormLayout;
    form->setLayout(lay_form);
    QLabel* denumire = new QLabel("Denumire");
    txtDenumire = new QLineEdit;
    QLabel* destinatie = new QLabel("Destinatie");
    txtProd = new QLineEdit;
    QLabel* tip = new QLabel("Tip");
    txtSubst = new QLineEdit;
    QLabel* pret = new QLabel("Pret");
    txtPret = new QLineEdit;

    lay_form->addRow(denumire, txtDenumire);
    lay_form->addRow(destinatie, txtDestinatie);
    lay_form->addRow(tip, txtTip);
    lay_form->addRow(pret, txtPret);

    lay_right->addWidget(form);

    QWidget* but_zone = new QWidget;
    QVBoxLayout* lay_but = new QVBoxLayout;
    but_zone->setLayout(lay_but);

    btn_add = new QPushButton("Add");
    lay_but->addWidget(btn_add);

    QWidget* sec_but = new QWidget;
    QHBoxLayout* sec_lay = new QHBoxLayout;
    sec_but->setLayout(sec_lay);

    btn_del = new QPushButton("Delete");
    btn_mod = new QPushButton("Update");
    sec_lay->addWidget(btn_del);
    sec_lay->addWidget(btn_mod);

    lay_but->addWidget(sec_but);

    btn_undo = new QPushButton("Undo");
    lay_but->addWidget(btn_undo);

    btn_cos_mst = new QPushButton("Generate Cos Master");
    lay_but->addWidget(btn_recipe_mst);
    btn_cos_rdonly = new QPushButton("Generate Cos Read-Only");
    lay_but->addWidget(btn_recipe_rdonly);

    lay_right->addWidget(but_zone);

    lyMain->addWidget(w_right);
    lb_index = -1;

    opt_but = new QWidget;
    lay_opt = new QVBoxLayout;
    opt_but->setLayout(lay_opt);
    lyMain->addWidget(opt_but);
    plm = new QSlider;
    plm->setMinimum(1);
    plm->setMaximum(100);
    lyMain->addWidget(plm);
}

void GUI::connectSignalsSlots() {
    QObject::connect(lmn, &QSlider::valueChanged, [=]() {
        txtPret>setText(QString::number(lmn->value()));
        });

    QObject::connect(btnSortDenumire, &QPushButton::clicked, [&]() {
        vector<Turism> turs;
        turs.resize(srv.get_all_ent().size());
        srv.sort(0, turs);
        reloadList(turs);
        });

    QObject::connect(btnSortDestinatie, &QPushButton::clicked, [&]() {
        vector<Turism> turs;
        turs.resize(srv.get_all_ent().size());
        srv.sort(1, turs);
        reloadList(turs);
        });

    QObject::connect(btnSortTP, &QPushButton::clicked, [&]() {
        vector<Turism> turs;
        turs.resize(srv.get_all_ent().size());
        srv.sort(2, turs);
        reloadList(turs);
        });

    QObject::connect(btn_add, &QPushButton::clicked, this, &GUI::addTur);
    QObject::connect(btn_del, &QPushButton::clicked, this, &GUI::delTur);
    QObject::connect(btn_mod, &QPushButton::clicked, this, &GUI::updTur);
    QObject::connect(btn_undo, &QPushButton::clicked, this, &GUI::undoTur);

    QObject::connect(btn_reset, &QPushButton::clicked, [=]() {
        reloadList(srv.get_all_ent());
        reset_form();
        });

    QObject::connect(btnFilterPret, &QPushButton::clicked, [=]() {
        string val_str = txtFilt->text().toStdString();
        try {
            vector<Turism> rez;
            rez.clear();
            srv.filter(0, val_str, rez);
            reloadList(rez);
        }
        catch (RepoException& re) {
            QMessageBox::warning(this, "Warning", QString::fromStdString(toMyString(re.msg)));
        }
        });

    QObject::connect(btnFilterDestinatie, &QPushButton::clicked, [=]() {
        string val_str = txtFilt->text().toStdString();
        try {
            vector<Turism> rez;
            rez.clear();
            srv.filter(1, val_str, rez);
            reloadList(rez);
        }
        catch (RepoException& re) {
            QMessageBox::warning(this, "Warning", QString::fromStdString(toMyString(re.msg)));
        }
        });

    QObject::connect(btn_cos_mst, &QPushButton::clicked, [=]() {
        auto wind = new CosGUI{ rep,srv };
        rcp.push_back(wind);
        wind->show();
        });

    QObject::connect(btn_cos_rdonly, &QPushButton::clicked, [=]() {
        auto wind = new PaintGUI{ rep };
        pg.push_back(wind);
        wind->show();
        });

    QObject::connect(lst_view->selectionModel(), &QItemSelectionModel::selectionChanged, [=]() {
        auto sel = lst_view->selectionModel();
        if (sel->selectedIndexes().empty()) {
            txtDenumire->setText("");
            txtTip->setText("");
            txtPret->setText("");
            txtDestinatie->setText("");
            return;
        }
        auto sel_index = sel->selectedIndexes().at(0).row();
        auto elem = act_list[sel_index];
        auto name = lst_view->model()->data(lst_view->model()->index(sel_index, 0), Qt::DisplayRole).toString();
        lb_index = sel_index;
        txtDenumire->setText(name);
        txtDestinatie->setText(QString::fromStdString(elem.get_destinatie()));
        txtTip->setText(QString::fromStdString(elem.get_tip()));
        txtPret->setText(QString::number(elem.get_pret()));
        });
}

void GUI::reloadList(vector<Turism>& turs) {
    act_list = turs;
    model->setTurs(turs);
    
}

void GUI::addTur() {
    try {
        srv.add(txtDenumire->text().toStdString(), txtDestinatie->text().toStdString(), txtTip->text().toStdString(), txtPret->text().toInt());
        reloadList(srv.get_all_ent());
        updateBut(srv.get_all_ent());
    }
    catch (ValidationException& ve) {
        QMessageBox::warning(this, "Warning", QString::fromStdString(toMyString(ve.msg)));
    }
    catch (RepoException& re) {
        QMessageBox::warning(this, "Warning", QString::fromStdString(toMyString(re.msg)));
    }
}

void GUI::delTur() {
    auto denumire = txtDenumire->text().toStdString();
    auto destinatie = txtDestinatie->text().toStdString();
    auto tip = txtTip->text().toStdString();
    auto pret = txtPret->text().toInt();
    auto t = Turism(denumire, destinatie, tip, pret);
    int index = 0;
    for (const auto& tur : srv.get_all_ent()) {
        if (tur == t) {
            break;
        }
        ++index;
    }
    if (index == srv.get_all_ent().size()) {
        QMessageBox::warning(this, "Warning", QString::fromStdString("Nu exista elementul introdus"));
    }
    else {
        srv.del(index);
        reloadList(srv.get_all_ent());
        updateBut(srv.get_all_ent());
    }
}

void GUI::updTur() {
    auto denumire = txtDenumire->text().toStdString();
    auto destinatie = txtDestinatie->text().toStdString();
    auto tip = txtTip->text().toStdString();
    auto pret = txtPret->text().toInt();

    if (lb_index == -1) {
        QMessageBox::warning(this, "Warning", QString::fromStdString("Nu ati selectat niciun element"));
        return;
    }

    try {
        srv.modify(lb_index, denumire, destinatie, tip, pret);
        reloadList(srv.get_all_ent());
        updateBut(srv.get_all_ent());
    }
    catch (ValidationException& ve) {
        QMessageBox::warning(this, "Warning", QString::fromStdString(toMyString(ve.msg)));
    }
}

void clearLayout(QLayout* layout) {
    if (layout == NULL)
        return;
    QLayoutItem* item;
    while ((item = layout->takeAt(0))) {
        if (item->layout()) {
            clearLayout(item->layout());
            delete item->layout();
        }
        if (item->widget()) {
            delete item->widget();
        }
        delete item;
    }
}

void GUI::updateBut(vector<Turism>& all) {
    clearLayout(lay_opt);
    set<string> unique;
    for (const auto& tur : srv.get_all_ent()) {
        unique.insert(tur.get_tip());
    }

    tip_but.clear();

    for (auto& it : unique) {
        subst_but.push_back(new QPushButton(QString::fromStdString(it)));
    }

    for (auto btn : tip_but) {
        lay_opt->addWidget(btn);
        QObject::connect(btn, &QPushButton::clicked, [=]() {
            auto val = btn->text().toStdString();
            int nr = 0;
            for (const auto& tur : srv.get_all_ent()) {
                if (med.get_tur() == val) {
                    ++nr;
                }
            }
            QMessageBox::information(nullptr, "Info", QString::number(nr));
            });
    }
}

void GUI::reset_form() {
    txtDenumire->setText("");
    txtDestinatie>setText("");
    txtTip->setText("");
    txtPret->setText("");
}

void GUI::undoTur() {
    try {
        srv.undo();
        reloadList(srv.get_all_ent());
        updateBut(srv.get_all_ent());
    }
    catch (RepoException& re) {
        QMessageBox::warning(this, "Warning", QString::fromStdString("Nu se mai poate face undo"));
    }
}

void RecipeGUI::initGUI() {
    setLayout(recipe_main_layout);

    cos_lst = new QListWidget;
    cos_main_layout->addWidget(recipe_lst);

    QWidget* cos_but_zone = new QWidget;
    QVBoxLayout* cos_but_layout = new QVBoxLayout;
    cos_but_zone->setLayout(cos_but_layout);

    QWidget* cos_form = new QWidget;
    QFormLayout* cos_form_layout = new QFormLayout;
    cos_form->setLayout(recipe_form_layout);

    QLabel* lbl_cos = new QLabel("Input");
    lne_cos = new QLineEdit;

    cos_form_layout->addRow(lbl_cos, lne_cos);

    cos_but_layout->addWidget(cos_form);

    add_to_cos = new QPushButton("Add");
    empty_cos = new QPushButton("Empty recipe");
    random_add = new QPushButton("Add random");
    export_cos = new QPushButton("Export");
    help_button = new QPushButton("Help");

    cos_but_layout->addWidget(add_to_cos);
    cos_but_layout->addWidget(empty_cos);
    cos_but_layout->addWidget(random_add);
    cos_but_layout->addWidget(export_cos);
    cos_but_layout->addWidget(help_button);

    cos_main_layout->addWidget(cos_but_zone);

    reloadTurs(rep.get_all());
}

void CosGUI::reloadTurs(vector<Turism> turs) {
    recipe_lst->clear();
    for (const auto& tur : turs) {
        QListWidgetItem* item = new QListWidgetItem(QString::fromStdString(tur.get_denumire()));
        recipe_lst->addItem(item);
    }
}

void CosGUI::connectSignals() {
    QObject::connect(add_to_cos, &QPushButton::clicked, [=]() {
        auto inp = lne_cos->text().toStdString();
        int nr = 0;
        bool valid = true;
        for (auto& ch : inp) {
            if ('0' <= ch && ch <= '9') {
                nr = nr * 10 + (ch - '0');
            }
            else {
                valid = false;
            }
        }
        if (nr > srv.get_all_ent().size()) {
            valid = false;
        }
        if (valid) {
            rep.add_to_cos(srv.get_all_ent()[nr]);
            reloadTurs(rep.get_all());
        }
        else {
            QMessageBox::warning(this, "Warning", QString::fromStdString("Index invalid"));
        }
        });

    QObject::connect(empty_cos, &QPushButton::clicked, [=]() {
        rep.empty_recipe();
        reloadTurs(rep.get_all());
        //reset_form();
        });

    QObject::connect(random_add, &QPushButton::clicked, [=]() {
        auto inp = lne_cos->text().toStdString();
        int nr = 0;
        bool valid = true;
        for (auto& ch : inp) {
            if ('0' <= ch && ch <= '9') {
                nr = nr * 10 + (ch - '0');
            }
            else {
                valid = false;
            }
        }
        if (valid) {
            rep.random_add(srv.get_all_ent(), nr);
            reloadTurs(rep.get_all());
        }
        else {
            QMessageBox::warning(this, "Warning", QString::fromStdString("Numar invalid"));
        }
        });

    QObject::connect(export_cos, &QPushButton::clicked, [=]() {
        auto filename = lne_cos->text().toStdString();
        rep.save_to_file(filename);
        });

    QObject::connect(help_button, &QPushButton::clicked, [=]() {
        string msg = "Campul input se foloseste pentru a comunica optiunile\n";
        msg += "Pentru Add in input se va specifica indicele de adaugat\n";
        msg += "Pentru Add random in input se va specifica numarul de entitati de adaugat\n";
        msg += "Pentru Export in input se va specifica numele fisierului in care se face exportul\n";
        QMessageBox::information(this, "Help", QString::fromStdString(msg));
        });
}