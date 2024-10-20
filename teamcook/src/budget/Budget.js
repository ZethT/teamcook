import React, { useState, useEffect } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CForm,
  CFormInput,
  CButton,
} from '@coreui/react'
import { CChart } from '@coreui/react-chartjs'

const BudgetApp = () => {
  const [totalIncome, setTotalIncome] = useState(0)
  const [expenses, setExpenses] = useState({})
  const [ingredientCount, setIngredientCount] = useState({})
  const [transactions, setTransactions] = useState([])
  const [income, setIncome] = useState('')
  const [expense, setExpense] = useState('')
  const [category, setCategory] = useState('')

  const addTransaction = () => {
    const incomeAmount = parseFloat(income) || 0
    const expenseAmount = parseFloat(expense) || 0

    setTotalIncome((prev) => prev + incomeAmount)

    if (expenseAmount > 0) {
      setExpenses((prev) => ({
        ...prev,
        [category]: (prev[category] || 0) + expenseAmount,
      }))
      setIngredientCount((prev) => ({
        ...prev,
        [category]: (prev[category] || 0) + 1,
      }))
    }

    setTransactions((prev) => [...prev, { income: incomeAmount, expense: expenseAmount, category }])

    setIncome('')
    setExpense('')
    setCategory('')
  }

  const pieChartData = {
    labels: Object.keys(expenses),
    datasets: [
      {
        data: Object.values(expenses),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
      },
    ],
  }

  const barChartData = {
    labels: Object.keys(ingredientCount),
    datasets: [
      {
        label: 'Ingredient Count',
        data: Object.values(ingredientCount),
        backgroundColor: '#36A2EB',
      },
    ],
  }

  const scatterChartData = {
    datasets: [
      {
        label: 'Cost vs Income',
        data: transactions.map((t) => ({ x: t.expense, y: t.income })),
        backgroundColor: '#FF6384',
      },
    ],
  }

  return (
    <CRow>
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardHeader>
            <strong>Budget App</strong>
            <div className="card-header-actions">
              <CButton color="link" className="card-header-action">
                Total Income: ${totalIncome.toFixed(2)}
              </CButton>
            </div>
          </CCardHeader>
          <CCardBody>
            <CForm className="row g-3">
              <CCol md={3}>
                <CFormInput
                  type="number"
                  id="income"
                  label="Income"
                  value={income}
                  onChange={(e) => setIncome(e.target.value)}
                />
              </CCol>
              <CCol md={3}>
                <CFormInput
                  type="number"
                  id="expense"
                  label="Expense"
                  value={expense}
                  onChange={(e) => setExpense(e.target.value)}
                />
              </CCol>
              <CCol md={3}>
                <CFormInput
                  type="text"
                  id="category"
                  label="Category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                />
              </CCol>
              <CCol xs={12}>
                <CButton color="primary" onClick={addTransaction}>
                  Add Transaction
                </CButton>
              </CCol>
            </CForm>
          </CCardBody>
        </CCard>
      </CCol>

      <CCol xs={12} md={4}>
        <CCard className="mb-4">
          <CCardHeader>Expense Categories</CCardHeader>
          <CCardBody>
            <CChart type="pie" data={pieChartData} />
          </CCardBody>
        </CCard>
      </CCol>

      <CCol xs={12} md={4}>
        <CCard className="mb-4">
          <CCardHeader>Ingredient Count</CCardHeader>
          <CCardBody>
            <CChart type="bar" data={barChartData} />
          </CCardBody>
        </CCard>
      </CCol>

      <CCol xs={12} md={4}>
        <CCard className="mb-4">
          <CCardHeader>Cost vs Income</CCardHeader>
          <CCardBody>
            <CChart type="scatter" data={scatterChartData} />
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default BudgetApp
