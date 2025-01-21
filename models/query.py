from typing import List, Any, Iterator
from .database import DataBase
from libs.common import date_format
from sqlalchemy.exc import IntegrityError
from libs.errors import UniqueViolationError
from datetime import datetime


class Query(DataBase):
    
    @property
    def columns(self):
        return [column for column in self.table.__table__.columns]
    
    def get_values(
        self, 
        page, 
        peer_page, 
        field, 
        key_value
        ) -> List[Any]:
        
        query = self.table.query
        
        if key_value:
            query = query.filter(getattr(self.table, field) == key_value)

        self.total = query.count()
        table_objs = query.offset((page - 1) * peer_page).limit(peer_page).all()
        self.total_pages = (self.total + peer_page - 1) // peer_page

        return [
            {
                column.name: date_format(
                    getattr(obj, column.name),
                    column.type,
                    'to_str'
                )
                for column in self.columns
            }
            for obj in table_objs
        ]

    
    def update_values(self, data, field, key_value) -> Iterator[List[Any]]:
        if isinstance(data, list):
            data = data[0]
            
        new_customer_data = {
            column.name: date_format(data.get(column.name), column.type, 'to_date')
            for column in self.columns
            if column.name in data
        }

        new_customer = self.table(**new_customer_data)

        existing_record = self.table.query.filter(
            getattr(self.table, field) == key_value).first()

        new_customer_data.update({
            'updated_at': datetime.today()
        })

        if existing_record:
            self.table.query.filter(
                getattr(self.table, field) == key_value).update(new_customer_data)
            self.db.session.commit() 
            rows = {
                column.name: date_format(
                getattr(
                    new_customer, 
                    column.name,
                    ),
                column.type,
                'to_str'
                ) for column in self.columns
                if column.name in data
            }
            return True, rows
        else:
            return False, f"User with field {field}:{key_value} not found."
    
    def remove_values(self, field, key_value):
        self.db.session.begin()
        
        try:   
            value = self.table.query.filter(getattr(self.table, field) == key_value).first()
            self.db.session.delete(value)        
            self.db.session.commit()
            return True
        except Exception:
            self.db.session.rollback()
            return False
        finally:
            self.db.session.close()
    
    def insert_values(self, data) -> List[Any]:
        output = []
        
        self.db.session.begin()
        for row in data:
            each_row = {
                column.name: date_format(row.get(column.name), column.type, 'to_date')
                for column in self.columns
                if column.name in row
            }
            each_row.update(
                {
                    'created_at': datetime.today()
                }
            )
            
            new_value = self.table(**each_row)
            self.db.session.add(new_value)

            try:
                self.db.session.flush()
                row.update({
                    'id': new_value.id
                })
                output.append(row)
                self.db.session.commit()
            except IntegrityError as e:
                self.db.session.rollback()
                output.append({
                    'error': str(str(e.orig)), 
                    'msg': UniqueViolationError.msg, 
                    'data': row
                })
            except Exception as e:
                self.db.session.rollback()
                output.append({
                    'error': str(str(e.orig)), 
                    'msg': str(e), 
                    'data': row
                })

        return output