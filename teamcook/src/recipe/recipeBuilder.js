import React, { useState, useRef, useEffect } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import Ingredient from './Ingredient'
import {
  CListGroup,
  CListGroupItem,
  CRow,
  CCol,
  CFormInput,
  CButton,
  CContainer,
  CFormTextarea,
  CSpinner,
  CAlert,
} from '@coreui/react'
import api from '../api'

const RecipeBuilder = () => {
  const { id } = useParams()
  const location = useLocation()
  const navigate = useNavigate()
  const { type } = location.state || {}

  const [ingredients, setIngredients] = useState([])
  const [recipeIngredients, setRecipeIngredients] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [recipeName, setRecipeName] = useState('')
  const [steps, setSteps] = useState([''])
  const [recipeType, setRecipeType] = useState(type || 'Processed')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        await fetchIngredients()
        if (id) {
          await fetchRecipe(id)
        }
      } catch (error) {
        console.error('Error fetching data:', error)
        setError('Failed to load data. Please try again.')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id])

  const fetchIngredients = async () => {
    const response = await api.get('/ingredients/')
    setIngredients(response.data)
  }

  const fetchRecipe = async (recipeId) => {
    const response = await api.get(`/recipes/${recipeId}`)
    const recipe = response.data
    setRecipeName(recipe.name)
    setRecipeType(recipe.type)
    setRecipeIngredients(recipe.ingredients || [])
    setSteps(recipe.steps?.map((step) => step.instruction) || [''])
  }

  const handleDragStart = (e, ingredient) => {
    e.dataTransfer.setData('application/json', JSON.stringify(ingredient))
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const droppedIngredient = JSON.parse(e.dataTransfer.getData('application/json'))

    if (!recipeIngredients.some((item) => item.id === droppedIngredient.id)) {
      setRecipeIngredients((prevIngredients) => [
        ...prevIngredients,
        {
          ...droppedIngredient,
          required_amount: 1,
          unit: droppedIngredient.unit,
        },
      ])
    }
  }

  const handleDeleteIngredient = (id) => {
    setRecipeIngredients((prevIngredients) =>
      prevIngredients.filter((ingredient) => ingredient.id !== id),
    )
  }

  const handleSave = async () => {
    const recipeData = {
      name: recipeName,
      type: recipeType,
      ingredients: recipeIngredients.map((ing) => ({
        id: ing.id,
        required_amount: ing.required_amount,
        unit: ing.unit,
      })),
      steps: steps.map((step, index) => ({
        step_number: index + 1,
        instruction: step,
      })),
    }

    try {
      if (id) {
        await api.put(`/recipes/${id}`, recipeData)
      } else {
        await api.post('/recipes/', recipeData)
      }
      navigate('/recipe-book')
    } catch (error) {
      console.error('Error saving recipe:', error)
      setError('Failed to save recipe. Please try again.')
    }
  }

  if (loading) {
    return (
      <CContainer
        className="d-flex justify-content-center align-items-center"
        style={{ height: '100vh' }}
      >
        <CSpinner />
      </CContainer>
    )
  }

  if (error) {
    return (
      <CContainer>
        <CAlert color="danger">{error}</CAlert>
      </CContainer>
    )
  }

  return (
    <CContainer fluid>
      <CRow className="mb-3 justify-content-between align-items-center">
        <CCol>
          <h2>{id ? 'Edit Recipe' : 'Create New Recipe'}</h2>
        </CCol>
        <CCol xs="auto">
          <CButton color="primary" onClick={handleSave}>
            Save Recipe
          </CButton>
        </CCol>
      </CRow>
      <CRow className="mb-3">
        <CCol>
          <CFormInput
            type="text"
            placeholder="Recipe Name"
            value={recipeName}
            onChange={(e) => setRecipeName(e.target.value)}
          />
        </CCol>
      </CRow>
      <CRow>
        {/* Ingredient search and list */}
        <CCol xs={12} md={3}>
          <CFormInput
            type="text"
            placeholder="Search ingredients..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="mb-3"
          />
          <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
            <CListGroup>
              {ingredients
                .filter((ingredient) =>
                  ingredient.name.toLowerCase().includes(searchQuery.toLowerCase()),
                )
                .map((ingredient) => (
                  <div
                    key={ingredient.id}
                    draggable
                    onDragStart={(e) => handleDragStart(e, ingredient)}
                  >
                    <Ingredient
                      ingredient={ingredient}
                      badgeColor={ingredient.type === 'Raw' ? 'success' : 'warning'}
                      badgeText={ingredient.type === 'Raw' ? 'RI' : 'PI'}
                    />
                  </div>
                ))}
            </CListGroup>
          </div>
        </CCol>

        {/* Recipe builder */}
        <CCol xs={12} md={5}>
          <div
            style={{
              minHeight: '400px',
              border: '2px dashed #ccc',
              padding: '10px',
              borderRadius: '4px',
            }}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <h4>Recipe Ingredients</h4>
            {recipeIngredients.length === 0 ? (
              <p>Drag ingredients here to build your recipe</p>
            ) : (
              <CListGroup>
                {recipeIngredients.map((ingredient) => (
                  <CListGroupItem
                    key={ingredient.id}
                    className="d-flex justify-content-between align-items-center"
                  >
                    <div>
                      {ingredient.name} ({ingredient.type})
                      <CFormInput
                        type="number"
                        value={ingredient.required_amount}
                        onChange={(e) => {
                          const updatedIngredients = recipeIngredients.map((ing) =>
                            ing.id === ingredient.id
                              ? { ...ing, required_amount: parseFloat(e.target.value) }
                              : ing,
                          )
                          setRecipeIngredients(updatedIngredients)
                        }}
                        style={{ width: '80px', display: 'inline-block', marginLeft: '10px' }}
                      />
                      <span style={{ marginLeft: '5px' }}>{ingredient.unit}</span>
                    </div>
                    <CButton
                      color="danger"
                      size="sm"
                      onClick={() => handleDeleteIngredient(ingredient.id)}
                    >
                      Delete
                    </CButton>
                  </CListGroupItem>
                ))}
              </CListGroup>
            )}
          </div>
        </CCol>

        {/* Recipe steps */}
        <CCol xs={12} md={4}>
          <h4>Recipe Steps</h4>
          {steps.map((step, index) => (
            <div key={index} className="mb-3">
              <CFormTextarea
                value={step}
                onChange={(e) => {
                  const newSteps = [...steps]
                  newSteps[index] = e.target.value
                  setSteps(newSteps)
                }}
                placeholder={`Step ${index + 1}`}
              />
              <CButton
                color="danger"
                size="sm"
                onClick={() => setSteps(steps.filter((_, i) => i !== index))}
                className="mt-2"
              >
                Delete Step
              </CButton>
            </div>
          ))}
          <CButton color="primary" onClick={() => setSteps([...steps, ''])}>
            Add Step
          </CButton>
        </CCol>
      </CRow>
    </CContainer>
  )
}

export default RecipeBuilder
