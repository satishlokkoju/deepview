import { render, fireEvent } from '@testing-library/svelte';
import Dropdown from '../../src/elements/Dropdown.svelte';
import { describe, test, expect } from 'vitest';

describe('Dropdown.svelte', () => {
  const items = ['Option 1', 'Option 2', 'Option 3'];

  test('renders correctly with items', () => {
    const { getAllByText } = render(Dropdown, { items, value: items[0] });
    items.forEach(item => {
      expect(getAllByText(item)[0]).toBeInTheDocument();
    });
  });

  test('selects the provided value', () => {
    const { container } = render(Dropdown, { items, value: items[1] });
    const select = container.querySelector('select');
    expect(select).not.toBeNull();
    expect(select?.value).toBe(items[1]);
  });

  test('updates when value changes', async () => {
    const { component, container } = render(Dropdown, { items, value: items[0] });
    
    const select = container.querySelector('select');
    expect(select).not.toBeNull();
    expect(select?.value).toBe(items[0]);

    await component.$set({ value: items[2] });
    expect(select?.value).toBe(items[2]);
  });

  test('triggers change event when selecting an option', async () => {
    const { container } = render(Dropdown, { items, value: items[0] });
    const select = container.querySelector('select');
    expect(select).not.toBeNull();

    // Change the value
    if (select) {
      await fireEvent.change(select, { target: { value: items[1] } });
      
      // Check if the value is updated
      expect(select.value).toBe(items[1]);
    }
  });
});
