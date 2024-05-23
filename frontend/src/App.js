import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    initialInterestRate: '',
    loanAmount: '',
    repaymentPeriodYears: '',
    salaries: '',
    splits: '',
    names: ''
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      salaries: formData.salaries.split(',').map(Number),
      splits: formData.splits.split(',').map(Number),
      names: formData.names.split(',')
    };
    try {
      const response = await axios.post('http://127.0.0.1:5000/calculate', payload);
      setResult(response.data);
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Loan Calculator</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="form-group">
          <label htmlFor="initialInterestRate">Initial Interest Rate</label>
          <input
            type="number"
            step="0.01"
            className="form-control"
            id="initialInterestRate"
            name="initialInterestRate"
            value={formData.initialInterestRate}
            onChange={handleChange}
            placeholder="Initial Interest Rate"
          />
        </div>
        <div className="form-group">
          <label htmlFor="loanAmount">Loan Amount</label>
          <input
            type="number"
            className="form-control"
            id="loanAmount"
            name="loanAmount"
            value={formData.loanAmount}
            onChange={handleChange}
            placeholder="Loan Amount"
          />
        </div>
        <div className="form-group">
          <label htmlFor="repaymentPeriodYears">Repayment Period (Years)</label>
          <input
            type="number"
            className="form-control"
            id="repaymentPeriodYears"
            name="repaymentPeriodYears"
            value={formData.repaymentPeriodYears}
            onChange={handleChange}
            placeholder="Repayment Period (Years)"
          />
        </div>
        <div className="form-group">
          <label htmlFor="salaries">Salaries (comma-separated)</label>
          <input
            type="text"
            className="form-control"
            id="salaries"
            name="salaries"
            value={formData.salaries}
            onChange={handleChange}
            placeholder="Salaries (comma-separated)"
          />
        </div>
        <div className="form-group">
          <label htmlFor="splits">Splits (comma-separated)</label>
          <input
            type="text"
            className="form-control"
            id="splits"
            name="splits"
            value={formData.splits}
            onChange={handleChange}
            placeholder="Splits (comma-separated)"
          />
        </div>
        <div className="form-group">
          <label htmlFor="names">Names (comma-separated)</label>
          <input
            type="text"
            className="form-control"
            id="names"
            name="names"
            value={formData.names}
            onChange={handleChange}
            placeholder="Names (comma-separated)"
          />
        </div>
        <button type="submit" className="btn btn-primary">Calculate</button>
      </form>
      {result && (
        <div className="result">
          <h3>Loan Calculation Result</h3>
          {result.payment_details.map((detail) => (
            <div key={detail.month}>
              <h4>Month {detail.month}</h4>
              <p>Remaining Loan Amount: {detail.remaining_loan_amount}</p>
              <p>Total Payment: {detail.total_payment}</p>
              <ul>
                {detail.borrowers.map((borrower, index) => (
                  <li key={index}>
                    {borrower.name} - Monthly Payment: {borrower.monthly_payment}, Principal Payment: {borrower.principal_payment}, Interest Cost: {borrower.interest_cost}, Effective Interest Rate: {borrower.effective_interest_rate}, Effective Monthly Payment: {borrower.effective_monthly_payment}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
