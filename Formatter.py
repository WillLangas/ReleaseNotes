class Formatter:
    
    def __init__(self):
        self.formatted_work_items = []

    def formatWorkItemNote(self, work_item):
        """
        Formats each work item as an HTML ordered list object according to the following format:
        - Title (Bold)
        - Generated Release Note
        - Work Item ID (Bold)

        Args:
            work_item (): _description_
        """
        result_str = f"<li><b>{work_item['Title']}:</b> {work_item['Generated_note']} <b>{work_item['ID']}</b></li>\n"
        self.formatted_work_items.append(result_str)

    def returnHTML(self):
        results = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="preconnect" href="https://fonts.gstatic.com">
                <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
                <title>Release Notes Template</title>

                <style type="text/css">
                    h1 { font-family: Poppins, Helvetica; font-weight: 400; font-size: large; color: #1B9CB9; }
                    ol { font-family: Poppins, Helvetica; font-size: medium;}

                </style>
            </head>
        <body>
            <h1>Upcoming Release: XXXX (Release Date XX/XX/XXXX) </h1>
            <ol>
        """

        for item in self.formatted_work_items:
            results += "\t\t" + item

        results += """   
            </ol>
        </body>
        </html>
        """

        return results