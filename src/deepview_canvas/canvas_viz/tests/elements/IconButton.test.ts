import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/svelte';
import IconButton from '../../src/elements/IconButton.svelte';

describe('IconButton.svelte', () => {
  it('renders with default (not filled) classes when no props are passed', () => {
    const { getByRole } = render(IconButton);
    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.className).includes('bg-white');
    expect(button.className).includes('text-button');
    expect(button.className).includes('border');
    expect(button.className).includes('border-button');
    expect(button.className).includes('rounded-md');
    expect(button.className).includes('py-1');
    expect(button.className).includes('px-2');
  });

  it('renders with default (not filled) classes when filled is false', () => {
    const { getByRole } = render(IconButton, { props: { filled: false } });
    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.className).includes('bg-white');
    expect(button.className).includes('text-button');
    expect(button.className).includes('border');
  });

  it('renders with filled classes when filled is true', () => {
    const { getByRole } = render(IconButton, { props: { filled: true } });
    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.className).includes('bg-button');
    expect(button.className).includes('text-text-dark');
    expect(button.className).not.includes('bg-white');
    expect(button.className).not.includes('text-button');
    expect(button.className).not.includes('border');
  });

  it('emits a click event when clicked', async () => {
    const handleClick = vi.fn();
    const { getByRole, component } = render(IconButton);
    component.$on('click', handleClick);

    const button = getByRole('button');
    await fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
