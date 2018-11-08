from orator.migrations import Migration


class CreateCompanyTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('company') as table:
            table.increments('id')
            table.text('name').nullable()
            table.text('url').nullable()
            table.text('ticker_symbol').nullable()
            table.text('country').nullable()
            table.text('business').nullable()
            table.text('listing_bourse').nullable()
            table.text('email').nullable()
            table.text('website').nullable()
            table.text('description').nullable()
            table.text('address').nullable()
            table.double('revenue').nullable()
            table.json('phone').nullable()
            table.json('auditing_company').nullable()
            table.json('financial_summary').nullable()
            table.json('business_registration').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('company')
