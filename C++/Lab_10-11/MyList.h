#pragma once

#include <QAbstractTableModel>
#include "domain.h"
#include <vector>

using std::vector;

class MyList :public QAbstractListModel {
    vector<Turism> turs;
public:
    MyList(const vector<Turism>& tur) : turs{ tur } {}


    int rowCount(const QModelIndex& parent = QModelIndex()) const override {
        return turs.size();
    }

    QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override {
        if (role == Qt::DisplayRole) {
            auto tt = turs[index.row()].get_denumire();
            return QString::fromStdString(tt);
        }
        return QVariant{};
    }

    void setTurs(vector<Turism>& tur) {
        turs = tur;
        auto topIndex = createIndex(0, 0);
        auto botIndex = createIndex(rowCount(), 0);
        emit dataChanged(topIndex, botIndex);
        emit layoutChanged();
    }
};
