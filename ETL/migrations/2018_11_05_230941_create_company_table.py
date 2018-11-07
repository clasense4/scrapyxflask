from orator.migrations import Migration


class CreateCompanyTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('company') as table:
            table.increments('id')
            table.text('name')
            table.text('url')
            table.text('ticker_symbol')
            table.text('country')
            table.text('business')
            table.text('listing_bourse')
            table.text('email')
            table.text('website')
            table.text('description')
            table.text('address')
            table.double('revenue')
            table.json('phone')
            table.json('auditing_company')
            table.json('financial_summary')
            table.json('business_registration')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('company')
