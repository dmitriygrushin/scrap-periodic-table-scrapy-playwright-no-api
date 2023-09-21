import copy
import json
import sqlite3


class GroupedElementsPipeline:
    def __init__(self):
        self.elems = {}

    def process_item(self, item, spider):
        # if the chemical_group has not been added to the elems dict
        cg = item["chemical_group"]
        if cg not in self.elems:
            self.elems[cg] = {
                    "element_count": 0,
                    "elements": []
                }

        # deleting the chemical group from the item so that it doesn't repeat in each instance
        #   of the item when it's in the self.elems dict
        item_copy = copy.deepcopy(item)
        del item_copy["chemical_group"]

        # append the dict representation of the item since the Scrapy Item may have trouble being serialized to JSON
        self.elems[cg]['elements'].append(dict(item))

        self.elems[cg]['elements_count'] += 1
        return item

    def close_spider(self, spider):
        with open("grouped_elements.json", "w") as f:
            json.dump(self.elems, f)





class ElementsPipeline:
    def __init__(self):
        self.conn = sqlite3.connect("elements.db")
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS periodic_elements(
            symbol TEXT PRIMARY KEY,
            name TEXT,
            atomic_number INTEGER, 
            atomic_mass REAL, 
            chemical_group TEXT)""")
        self.conn.commit()

    def process_item(self, item, spider):
        # To avoid sql injections use a layer of separation b/w the str that gets exec on the db server
        #   and the data from the outside world. We do that by no building the str manually,
        #   but delegate it to the cursor/db-driver.
        # Instead of using an f str we build the str, then separately pass in the data that should replace the ?s
        self.cursor.execute("INSERT OR IGNORE INTO periodic_elements VALUES (?, ?, ?, ?, ?)",
                            (
                                item["symbol"],
                                item["name"],
                                item["atomic_number"],
                                item["atomic_mass"],
                                item["chemical_group"]))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # eventually garbage collected, but this is good practice
        self.conn.close()
