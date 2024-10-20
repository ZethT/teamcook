import React from 'react'
import { CListGroup, CListGroupItem, CRow, CCol, CFormInput, CButton } from '@coreui/react'

const RecipeBook = () => {
  return (
    <>
      <CRow>
        {/* SEARCH BAR */}
        <CCol xs={6} >
        {/* Flex container for Search bar and Create New button */}
        <div className="d-flex align-items-center mb-3">
          {/* Search Bar */}
          <CFormInput
            type="text"
            placeholder="Search..."
            onChange={(e) => setSearchQuery(e.target.value)}
            className="me-2"
          />
          
          {/* Create New Button */}
          <CButton color="primary">Create New</CButton>
        </div>

        {/* Scrollable Group List */}
        <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
          <CListGroup>
            <CListGroupItem as="a" href="#" active>
              <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">List group item heading</h5>
                <small>3 days ago</small>
              </div>
              <p className="mb-1">
                Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.
              </p>
              <small>Donec id elit non mi porta.</small>
            </CListGroupItem>
            {/* Add more CListGroupItem as needed */}
            <CListGroupItem as="a" href="#">
              <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">Another item heading</h5>
                <small className="text-body-secondary">3 days ago</small>
              </div>
              <p className="mb-1">
                Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.
              </p>
              <small className="text-body-secondary">Donec id elit non mi porta.</small>
            </CListGroupItem>
            {/* Continue adding items as needed */}
          </CListGroup>
        </div>
      </CCol>

      <CCol xs={6} >
        {/* Flex container for Search bar and Create New button */}
        <div className="d-flex align-items-center mb-3">
          {/* Search Bar */}
          <CFormInput
            type="text"
            placeholder="Search..."
            onChange={(e) => setSearchQuery(e.target.value)}
            className="me-2"
          />
          
          {/* Create New Button */}
          <CButton color="primary">Create New</CButton>
        </div>

        {/* Scrollable Group List */}
        <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
          <CListGroup>
            <CListGroupItem as="a" href="#" active>
              <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">List group item heading</h5>
                <small>3 days ago</small>
              </div>
              <p className="mb-1">
                Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.
              </p>
              <small>Donec id elit non mi porta.</small>
            </CListGroupItem>
            {/* Add more CListGroupItem as needed */}
            <CListGroupItem as="a" href="#">
              <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">Another item heading</h5>
                <small className="text-body-secondary">3 days ago</small>
              </div>
              <p className="mb-1">
                Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.
              </p>
              <small className="text-body-secondary">Donec id elit non mi porta.</small>
            </CListGroupItem>
            {/* Continue adding items as needed */}
          </CListGroup>
        </div>
      </CCol>
      </CRow>
    </>
  )
}

export default RecipeBook
