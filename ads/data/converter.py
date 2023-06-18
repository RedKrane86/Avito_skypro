import csv
import json


def csv_to_json(csv_f, json_f, model):
    result = []
    with open(csv_f, encoding='utf-8') as c_file:
        csv_reader = csv.DictReader(c_file)

        for row in csv_reader:
            if "is_published" in row:
                if row["is_published"] == 'TRUE':
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            if "location_id" in row:
                row["location"] = [row["location_id"]]
                del row["location_id"]
            result.append({'model': model, 'fields': row})

    with open(json_f, 'w', encoding='utf-8') as j_file:
        json_string = json.dumps(result, indent=4, ensure_ascii=False)
        j_file.write(json_string)


if __name__ == '__main__':
    csv_to_json('ad.csv', 'ad.json', 'ads.ad')
    csv_to_json('category.csv', 'category.json', 'ads.category')
    csv_to_json("user.csv", "user.json", "ads.user")
    csv_to_json("location.csv", "location.json", "ads.location")
