export const exampleData = {
  users: [
    {
      user_id: "R002",
      name: "FreshMart Supermarket",
      business_type: "Supermarket Chain",
      location: "Bangalore",
      annual_revenue: 40000000,
      business_income: 12000000,
      sales: {
        monthly_sales: 3500000,
        online_sales: 1000000,
        offline_sales: 2500000
      },
      inventory: {
        total_value: 8000000,
        categories: [
          { category: "Groceries", value: 3000000 },
          { category: "Dairy & Beverages", value: 1500000 },
          { category: "Electronics", value: 1000000 },
          { category: "Personal Care", value: 1500000 }
        ]
      },
      expenses: {
        rent: 1200000,
        salaries: 5000000,
        utilities: 500000,
        marketing: 700000,
        insurance: 400000,
        logistics: 1500000,
        total_expenses: 9300000
      },
      profit_and_loss: {
        total_income: 12000000,
        total_expenses: 9300000,
        net_profit: 2700000
      },
      assets: {
        real_estate: [
          { type: "Supermarket Premises", location: "Bangalore", value: 15000000 }
        ]
      },
      loans: {
        business_loan: {
          outstanding: 6300000
        }
      },
      debt_liabilities: {
        credit_card_debt: 200000
      }
    }
  ]
};