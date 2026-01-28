import React from 'react';
import { Filter, Map, RotateCcw } from 'lucide-react';
import { CRIME_TYPES } from '../utils/constants';
import '../styles/components.css'; // Assuming you have this from previous steps

export default function Sidebar({ filters, toggles, onFilterChange, onToggleChange, onReset }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <h3><Filter size={16} /> Filters</h3>
        
        <div className="control-group">
          <label>Crime Type</label>
          <select 
            value={filters.crimeType} 
            onChange={(e) => onFilterChange('crimeType', e.target.value)}
          >
            <option value="All">All Categories</option>
            {Object.values(CRIME_TYPES).map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="sidebar-separator" />

      <div className="sidebar-section">
        <h3><Map size={16} /> Layers</h3>
        <div className="toggle-row">
          <label>Heatmap</label>
          <input 
            type="checkbox" 
            checked={toggles.showHeatmap} 
            onChange={() => onToggleChange('showHeatmap')} 
          />
        </div>
        <div className="toggle-row">
          <label>Hotspots</label>
          <input 
            type="checkbox" 
            checked={toggles.showHotspots} 
            onChange={() => onToggleChange('showHotspots')} 
          />
        </div>
      </div>

      <div className="sidebar-footer">
        <button className="btn-reset" onClick={onReset}>
          <RotateCcw size={14} /> Reset
        </button>
      </div>
    </aside>
  );
}