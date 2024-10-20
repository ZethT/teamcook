import React, { useState, useEffect } from 'react'
import {
  CRow,
  CCol,
  CFormInput,
  CButton,
  CDropdown,
  CDropdownToggle,
  CDropdownMenu,
  CDropdownItem,
  CAlert,
} from '@coreui/react'

import api from '../api'

const Testing = () => {
  // State variables for each action
  // Action 1: Add Stock
  const [ingredients, setIngredients] = useState([])
  const [selectedIngredient, setSelectedIngredient] = useState(null)
  const [amount, setAmount] = useState('')
  const [unit, setUnit] = useState('')
  const [cost, setCost] = useState('')

  // Action 2: Execute Processed Recipe
  const [processedRecipes, setProcessedRecipes] = useState([])
  const [selectedProcessedRecipe, setSelectedProcessedRecipe] = useState(null)
  const [quantityToProduce, setQuantityToProduce] = useState('')

  // Action 3: Execute Full Recipe
  const [fullRecipes, setFullRecipes] = useState([])
  const [selectedFullRecipe, setSelectedFullRecipe] = useState(null)
  const [quantityToPrepare, setQuantityToPrepare] = useState('')
  const [salePrice, setSalePrice] = useState('')

  // General
  const [message, setMessage] = useState('')

  // Fetch data on component mount
  useEffect(() => {
    // Fetch ingredients for Action 1
    api
      .get('/ingredients/')
      .then((response) => {
        setIngredients(response.data.filter((ingredient) => ingredient.type === 'Raw'))
      })
      .catch((error) => {
        console.error('Error fetching ingredients:', error)
      })

    // Fetch recipes for Actions 2 and 3
    api
      .get('/recipes/')
      .then((response) => {
        setProcessedRecipes(response.data.filter((recipe) => recipe.type === 'Processed'))
        setFullRecipes(response.data.filter((recipe) => recipe.type === 'Full Recipe'))
      })
      .catch((error) => {
        console.error('Error fetching recipes:', error)
      })
  }, [])

  // Action 1: Add Stock
  const handleSelectIngredient = (ingredient) => {
    setSelectedIngredient(ingredient)
    setUnit(ingredient.unit)
  }

  const handleAddStock = () => {
    if (!selectedIngredient || !amount || !cost) {
      setMessage('Please select an ingredient and enter amount and cost.')
      return
    }

    // Create stock entry
    api
      .post('/stocks/', {
        name: `${selectedIngredient.name} Stock`,
        expiry_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days from now
        cost: parseFloat(cost),
        amount: parseFloat(amount),
        unit: selectedIngredient.unit,
        ingredient_id: selectedIngredient.id,
      })
      .then((response) => {
        setMessage('Stock added successfully.')
        // Reset form
        setSelectedIngredient(null)
        setAmount('')
        setCost('')
        setUnit('')
      })
      .catch((error) => {
        console.error('Error adding stock:', error)
        setMessage('Error adding stock: ' + error.response?.data?.message || error.message)
      })
  }

  // Action 2: Execute Processed Recipe
  const handleExecuteProcessedRecipe = () => {
    if (!selectedProcessedRecipe || !quantityToProduce) {
      setMessage('Please select a recipe and enter a quantity.')
      return
    }

    api
      .post('/execute_processed_recipe', {
        recipe_id: selectedProcessedRecipe.id,
        quantity: parseFloat(quantityToProduce),
      })
      .then((response) => {
        setMessage('Processed recipe executed successfully.')
        // Reset form
        setSelectedProcessedRecipe(null)
        setQuantityToProduce('')
      })
      .catch((error) => {
        console.error('Error executing processed recipe:', error)
        setMessage(
          'Error executing processed recipe: ' + error.response?.data?.message || error.message,
        )
      })
  }

  // Action 3: Execute Full Recipe
  const handleExecuteFullRecipe = () => {
    if (!selectedFullRecipe || !quantityToPrepare || !salePrice) {
      setMessage('Please select a recipe, enter quantity and sale price.')
      return
    }

    api
      .post('/execute_full_recipe', {
        recipe_id: selectedFullRecipe.id,
        quantity: parseFloat(quantityToPrepare),
        sale_price: parseFloat(salePrice),
      })
      .then((response) => {
        setMessage('Full recipe executed and sale recorded successfully.')
        // Reset form
        setSelectedFullRecipe(null)
        setQuantityToPrepare('')
        setSalePrice('')
      })
      .catch((error) => {
        console.error('Error executing full recipe:', error)
        setMessage('Error executing full recipe: ' + error.response?.data?.message || error.message)
      })
  }

  return (
    <div style={{ padding: '20px' }}>
      {message && <CAlert color="info">{message}</CAlert>}

      {/* Action 1: Add Stock */}
      <h2>Action 1: Add Stock</h2>
      <CRow className="align-items-center mb-4">
        <CCol sm={3}>
          <CDropdown>
            <CDropdownToggle color="secondary">
              {selectedIngredient ? selectedIngredient.name : 'Select Ingredient'}
            </CDropdownToggle>
            <CDropdownMenu>
              {ingredients.map((ingredient) => (
                <CDropdownItem
                  key={ingredient.id}
                  onClick={() => handleSelectIngredient(ingredient)}
                >
                  {ingredient.name}
                </CDropdownItem>
              ))}
            </CDropdownMenu>
          </CDropdown>
        </CCol>
        <CCol sm={3}>
          <CFormInput
            type="number"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
        </CCol>
        <CCol sm={2}>
          <CFormInput
            type="number"
            placeholder="Cost"
            value={cost}
            onChange={(e) => setCost(e.target.value)}
          />
        </CCol>
        <CCol sm={2}>
          <CFormInput type="text" placeholder="Unit" value={unit} disabled />
        </CCol>
        <CCol sm={2}>
          <CButton color="primary" onClick={handleAddStock}>
            Submit
          </CButton>
        </CCol>
      </CRow>

      {/* Action 2: Execute Processed Recipe */}
      <h2>Action 2: Execute Processed Recipe</h2>
      <CRow className="align-items-center mb-4">
        <CCol sm={8}>
          <CDropdown>
            <CDropdownToggle color="secondary">
              {selectedProcessedRecipe ? selectedProcessedRecipe.name : 'Select Processed Recipe'}
            </CDropdownToggle>
            <CDropdownMenu>
              {processedRecipes.map((recipe) => (
                <CDropdownItem key={recipe.id} onClick={() => setSelectedProcessedRecipe(recipe)}>
                  {recipe.name}
                </CDropdownItem>
              ))}
            </CDropdownMenu>
          </CDropdown>
        </CCol>
        <CCol sm={2}>
          <CFormInput
            type="number"
            placeholder="Quantity"
            value={quantityToProduce}
            onChange={(e) => setQuantityToProduce(e.target.value)}
          />
        </CCol>
        <CCol sm={2}>
          <CButton color="primary" onClick={handleExecuteProcessedRecipe}>
            Submit
          </CButton>
        </CCol>
      </CRow>

      {/* Action 3: Execute Full Recipe */}
      <h2>Action 3: Execute Full Recipe</h2>
      <CRow className="align-items-center mb-4">
        <CCol sm={3}>
          <CDropdown>
            <CDropdownToggle color="secondary">
              {selectedFullRecipe ? selectedFullRecipe.name : 'Select Full Recipe'}
            </CDropdownToggle>
            <CDropdownMenu>
              {fullRecipes.map((recipe) => (
                <CDropdownItem key={recipe.id} onClick={() => setSelectedFullRecipe(recipe)}>
                  {recipe.name}
                </CDropdownItem>
              ))}
            </CDropdownMenu>
          </CDropdown>
        </CCol>
        <CCol sm={3}>
          <CFormInput
            type="number"
            placeholder="Quantity"
            value={quantityToPrepare}
            onChange={(e) => setQuantityToPrepare(e.target.value)}
          />
        </CCol>
        <CCol sm={3}>
          <CFormInput
            type="number"
            placeholder="Sale Price"
            value={salePrice}
            onChange={(e) => setSalePrice(e.target.value)}
          />
        </CCol>
        <CCol sm={3}>
          <CButton color="primary" onClick={handleExecuteFullRecipe}>
            Submit
          </CButton>
        </CCol>
      </CRow>
    </div>
  )
}

export default Testing
